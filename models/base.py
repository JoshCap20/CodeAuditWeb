from pydantic import BaseModel, HttpUrl
from typing import TypeVar, Generic


class Base(BaseModel):
    """Abstract base class for all models."""

    pass


class BaseMeasurement(Base):
    """Abstract base class for measurements."""

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


BTM = TypeVar("BTM", bound="BaseTimeMeasurement")


class BaseTimeMeasurement(BaseMeasurement, Generic[BTM]):
    """Abstract class for time measurements."""

    milliseconds: float
    seconds: float
    minutes: float

    @classmethod
    def from_seconds(cls, seconds: float) -> BTM:
        return cls(milliseconds=seconds * 1000, seconds=seconds, minutes=seconds / 60)  # type: ignore


BSM = TypeVar("BSM", bound="BaseSizeMeasurement")


class BaseSizeMeasurement(BaseMeasurement, Generic[BSM]):
    """Abstract class for size measurements."""

    kilobytes: float
    megabytes: float
    gigabytes: float

    @classmethod
    def from_mebibyte(cls, mebibyte: float) -> BSM:
        return cls(
            kilobytes=mebibyte * 1024, megabytes=mebibyte, gigabytes=mebibyte / 1024
        )  # type: ignore


class FileLink(Base):
    """Model for representing a file link."""
    
    url: HttpUrl

    def __str__(self):
        return self.url
    
    @classmethod
    def from_path(cls, file: str) -> "FileLink":
        path: HttpUrl = HttpUrl.build(scheme="file", host="", path=file)
        return cls(url=path)
