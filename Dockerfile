FROM nvidia/cuda:12.2.2-base-ubuntu22.04 AS base

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
    python3 python3-dev python3-pip git build-essential ffmpeg cmake wget libssl-dev

RUN apt install -y git

RUN wget https://github.com/Kitware/CMake/releases/download/v3.20.3/cmake-3.20.3.tar.gz \
    && tar -zxvf cmake-3.20.3.tar.gz \
    && cd cmake-3.20.3 \
    && ./bootstrap && make && make install \
    && rm -rf cmake-3.20.3 cmake-3.20.3.tar.gz

RUN pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

RUN pip install numpy==1.26.4

RUN git clone https://github.com/SHI-Labs/NATTEN \
    && cd NATTEN \
    && make \
    && pip install . \
    && rm -rf NATTEN

RUN pip install ninja git+https://github.com/CPJKU/madmom

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS api

COPY . .

RUN pip install .

RUN pip install fastapi uvicorn mutagen huggingface_hub[cli]

RUN huggingface-cli download taejunkim/allinone

ENTRYPOINT [ "/bin/bash", "-c" ]
CMD ["uvicorn app:app --host 0.0.0.0 --port 30000"]