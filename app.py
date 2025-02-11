import warnings
from logging import getLogger
import os
import subprocess
import tempfile
from urllib import request
from fastapi import FastAPI
from mutagen.mp3 import MP3
from pydantic import BaseModel

from allin1 import analyze
from allin1.typings import AnalysisResult

warnings.filterwarnings("ignore")

OUT_DIR = "/tmp/struct"
DEMIX_DIR = "/tmp/demix"
SPEC_DIR = "/tmp/spec"


logger = getLogger("uvicorn")

app = FastAPI(title="Musicbeats")


class Segment(BaseModel):
    start: float
    end: float
    label: str


class AudioMetadata(BaseModel):
    duration: float
    bpm: int
    beats: list[float]
    downbeats: list[float]
    beat_positions: list[int]
    segments: list[Segment]


def get_audio_duration(file_path):
    audio = MP3(file_path)
    duration = audio.info.length
    return duration


def trim_audio(input_path, output_path, duration):
    command = [
        "ffmpeg",
        "-i",
        input_path,  # Исходный файл
        "-y",
        "-ss",
        "0",  # Начать с начала
        "-t",
        str(duration),  # Продолжительность обрезки
        "-c",
        "copy",  # Копировать аудио без перекодировки
        output_path,
    ]

    subprocess.run(command)

    return output_path


@app.get(
    "/analyze",
    name="audio",
    response_model=AudioMetadata,
)
def audio_analyze(
    file_url: str,
    max_duration: float = 90,
):
    _, file_path = tempfile.mkstemp(dir="/tmp", suffix=".mp3")
    request.urlretrieve(file_url, file_path)

    duration = get_audio_duration(file_path)
    logger.info(f"Duration: {duration}")

    if duration > max_duration:
        logger.info(f"Trimming audio to {max_duration} seconds")
        path_extension = os.path.splitext(file_path)[-1]
        trimmed_file_path = file_path.replace(
            path_extension, "_trimmed" + path_extension
        )
        file_path = trim_audio(
            file_path,
            trimmed_file_path,
            max_duration,
        )

    logger.info(f"Analyzing audio file: {file_path}")
    analysis_result: AnalysisResult = analyze(
        file_path,
        out_dir=OUT_DIR,
        demix_dir=DEMIX_DIR,
        spec_dir=SPEC_DIR,
        overwrite=True,
        multiprocess=False,
        model="harmonix-all",
        # model="harmonix-fold0",
        # include_activations=True,
    )

    logger.info("Analysis complete. Cleaning up...")
    os.remove(file_path)

    return {
        "duration": duration,
        "bpm": analysis_result.bpm,
        "beats": analysis_result.beats,
        "downbeats": analysis_result.downbeats,
        "beat_positions": analysis_result.beat_positions,
        "segments": [
            {
                "start": seg.start,
                "end": seg.end,
                "label": seg.label,
            }
            for seg in analysis_result.segments
        ],
    }
