from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.segment import Segment


T = TypeVar("T", bound="AudioMetadata")


@_attrs_define
class AudioMetadata:
    """
    Attributes:
        duration (float):
        bpm (int):
        beats (List[float]):
        downbeats (List[float]):
        beat_positions (List[int]):
        segments (List['Segment']):
    """

    duration: float
    bpm: int
    beats: List[float]
    downbeats: List[float]
    beat_positions: List[int]
    segments: List["Segment"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        duration = self.duration

        bpm = self.bpm

        beats = self.beats

        downbeats = self.downbeats

        beat_positions = self.beat_positions

        segments = []
        for segments_item_data in self.segments:
            segments_item = segments_item_data.to_dict()
            segments.append(segments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "duration": duration,
                "bpm": bpm,
                "beats": beats,
                "downbeats": downbeats,
                "beat_positions": beat_positions,
                "segments": segments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.segment import Segment

        d = src_dict.copy()
        duration = d.pop("duration")

        bpm = d.pop("bpm")

        beats = cast(List[float], d.pop("beats"))

        downbeats = cast(List[float], d.pop("downbeats"))

        beat_positions = cast(List[int], d.pop("beat_positions"))

        segments = []
        _segments = d.pop("segments")
        for segments_item_data in _segments:
            segments_item = Segment.from_dict(segments_item_data)

            segments.append(segments_item)

        audio_metadata = cls(
            duration=duration,
            bpm=bpm,
            beats=beats,
            downbeats=downbeats,
            beat_positions=beat_positions,
            segments=segments,
        )

        audio_metadata.additional_properties = d
        return audio_metadata

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
