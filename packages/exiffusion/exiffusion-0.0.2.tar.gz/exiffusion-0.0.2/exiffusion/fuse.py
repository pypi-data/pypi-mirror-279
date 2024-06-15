from pathlib import Path, PosixPath
from datetime import datetime
import os
import logging

from typing import List

from rich.progress import track

from exiffusion.exif import get_exif
from exiffusion.geo import dms_to_location
from exiffusion.overlay import overlay_text

log = logging.getLogger(__name__)


def fuse_exif(path: str | PosixPath, output_dir: str | PosixPath):
    imgs = []

    if os.path.isdir(path):
        heic = sorted(Path(path).glob("*.heic", case_sensitive=False))
        jpg = sorted(Path(path).glob("*.jpg", case_sensitive=False))
        jpeg = sorted(Path(path).glob("*.jpeg", case_sensitive=False))

        imgs = heic + jpg + jpeg
    elif os.path.isfile(path):
        imgs = [Path(path)]

    if len(imgs) == 0:
        log.info("No valid images found.")
        return

    imgs = process_images(imgs, output_dir)

    return imgs


def process_images(
    imgs: List[str | PosixPath], output_dir: str | PosixPath
) -> List[str | PosixPath]:
    successes = []
    failures = []

    for img in track(imgs, description="Processing..."):
        log.info(f"Processing: {img}")
        try:
            exif_tags = get_exif(img)

            formatted_datetime = datetime.strptime(
                exif_tags.DateTime, "%Y:%m:%d %H:%M:%S"
            ).strftime("%Y-%m-%d %H:%M:%S")

            if (
                exif_tags.GPSLatitude is not None
                and exif_tags.GPSLatitudeRef is not None
                and exif_tags.GPSLongitude is not None
                and exif_tags.GPSLongitudeRef is not None
            ):
                location = dms_to_location(
                    exif_tags.GPSLatitudeRef,
                    exif_tags.GPSLatitude,
                    exif_tags.GPSLongitudeRef,
                    exif_tags.GPSLongitude,
                )

                if location.city is not None and location.country is not None:
                    text = f"{formatted_datetime}\n{location.city}, {location.country}"
                elif location.country is not None and location.address is not None:
                    text = f"{formatted_datetime}\n{location.address.split(',')[0]}, {location.country}"
                elif location.country is not None and location.state is not None:
                    text = f"{formatted_datetime}\n{location.state}, {location.country}\n{round(location.latitude, 4)}, {round(location.longitude, 4)}"
                elif (
                    location.country is not None
                    and location.latitude is not None
                    and location.longitude is not None
                ):
                    text = f"{formatted_datetime}\n{location.country}\n{round(location.latitude, 4)}, {round(location.longitude, 4)}"
                else:
                    text = f"{formatted_datetime}"
            else:
                text = f"{formatted_datetime}"

            overlay_text(img, text, output_dir)
            successes.append(img)
        except Exception as e:
            log.error(f"Failed to process {img}. Error: {e}")
            failures.append(img)

    log.info(f"Successfully processed: {successes}.")

    if failures:
        log.warn(f"Failed to process: {failures}")

    return imgs
