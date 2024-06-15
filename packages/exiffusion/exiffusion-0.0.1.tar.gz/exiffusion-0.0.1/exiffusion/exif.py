from PIL import Image
from PIL.Image import Exif
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener

from typing import Tuple, Optional
from pydantic import BaseModel
from pathlib import PosixPath
import logging

register_heif_opener()

GPSINFO_IFD_KEY = 34853
GENERAL_IFD_KEY = 34665

log = logging.getLogger(__name__)


class TopLevelExifTags(BaseModel):
    Orientation: Optional[int] = 1
    DateTime: str
    Make: Optional[str] = None
    Model: Optional[str] = None
    HostComputer: Optional[str] = None
    Software: Optional[str] = None


class GPSExifTags(BaseModel):
    GPSLatitudeRef: Optional[str] = None
    GPSLatitude: Optional[Tuple[float, float, float]] = None
    GPSLongitudeRef: Optional[str] = None
    GPSLongitude: Optional[Tuple[float, float, float]] = None


class GeneralIFDTags(BaseModel):
    ShutterSpeedValue: Optional[float] = None
    ApertureValue: Optional[float] = None
    DateTimeOriginal: Optional[str] = None
    DateTimeDigitized: Optional[str] = None
    BrightnessValue: Optional[float] = None
    ExposureBiasValue: Optional[float] = None
    MeteringMode: Optional[int] = None
    ColorSpace: Optional[int] = None
    Flash: Optional[int] = None
    FocalLength: Optional[float] = None
    ExifImageWidth: Optional[int] = None
    ExifImageHeight: Optional[int] = None
    FocalLengthIn35mmFilm: Optional[int] = None
    OffsetTime: Optional[str] = None
    SubsecTimeOriginal: Optional[str] = None
    SubjectLocation: Optional[Tuple[int, int, int, int]] = None
    SubsecTimeDigitized: Optional[str] = None
    SensingMethod: Optional[int] = None
    ExposureTime: Optional[float] = None
    FNumber: Optional[float] = None
    SceneType: Optional[int] = None
    ExposureProgram: Optional[int] = None
    ISOSpeedRatings: Optional[int] = None
    ExposureMode: Optional[int] = None
    WhiteBalance: Optional[int] = None
    LensSpecification: Optional[Tuple[float, float, float, float]] = None
    LensMake: Optional[str] = None
    LensModel: Optional[str] = None
    CompositeImage: Optional[int] = None
    # MakerNote: Optional[bytes] = None


class RelevantExifTags(TopLevelExifTags, GPSExifTags, GeneralIFDTags):
    pass


def get_exif(img: str | PosixPath, get_detailed_tags=False) -> RelevantExifTags:
    log.info(f"Getting Exif data from {img}.")

    image = Image.open(img)
    exif = image.getexif()

    relevant_tags = [
        "Orientation",
        "DateTime",
        "Make",
        "Model",
        "HostComputer",
        "Software",
    ]

    exif_tags = {}

    for tag, value in exif.items():
        if tag in TAGS:
            if TAGS[tag] in relevant_tags:
                exif_tags[TAGS[tag]] = value

    gps_tags = get_gps(exif)

    if get_detailed_tags:
        general_tags = get_general_ifd(exif)

        return RelevantExifTags(
            **(exif_tags | gps_tags.model_dump() | general_tags.model_dump())
        )
    else:
        return RelevantExifTags(**(exif_tags | gps_tags.model_dump()))


def get_gps(exif: Exif) -> GPSExifTags:
    gps_info = exif.get_ifd(GPSINFO_IFD_KEY)

    relevant_tags = ["GPSLatitudeRef", "GPSLatitude", "GPSLongitudeRef", "GPSLongitude"]

    gps_tags = {}

    for tag, value in gps_info.items():
        gps_tag = GPSTAGS.get(tag, tag)
        if gps_tag in relevant_tags:
            gps_tags[gps_tag] = value

    return GPSExifTags(**gps_tags)


def get_general_ifd(exif: Exif) -> GeneralIFDTags:
    general_ifd = exif.get_ifd(GENERAL_IFD_KEY)

    relevant_tags = [
        "ShutterSpeedValue",
        "ApertureValue",
        "DateTimeOriginal",
        "DateTimeDigitized",
        "BrightnessValue",
        "ExposureBiasValue",
        "MeteringMode",
        "ColorSpace",
        "Flash",
        "FocalLength",
        "ExifImageWidth",
        "ExifImageHeight",
        "FocalLengthIn35mmFilm",
        "OffsetTime",
        "SubsecTimeOriginal",
        "SubjectLocation",
        "SubsecTimeDigitized",
        "SensingMethod",
        "ExposureTime",
        "FNumber",
        "SceneType",
        "ExposureProgram",
        "ISOSpeedRatings",
        "ExposureMode",
        "WhiteBalance",
        "LensSpecification",
        "LensMake",
        "LensModel",
        "CompositeImage",
        # "MakerNote",
    ]

    ifd_tags = {}

    for tag, value in general_ifd.items():
        ifd_tag = TAGS.get(tag, tag)

        if ifd_tag in relevant_tags:
            ifd_tags[ifd_tag] = value

    if "SceneType" in ifd_tags:
        ifd_tags["SceneType"] = ord(ifd_tags["SceneType"])

    return GeneralIFDTags(**ifd_tags)
