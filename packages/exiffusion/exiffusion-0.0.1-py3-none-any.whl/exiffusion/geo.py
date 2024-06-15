import functools
import logging

from typing import Tuple, Optional
from pydantic import BaseModel

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

log = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="ExifFusion")

reverse_limit = RateLimiter(
    geolocator.reverse,
    min_delay_seconds=1,
    max_retries=4,
)

reverse = functools.lru_cache(maxsize=1024)(functools.partial(reverse_limit, timeout=5))


class Location(BaseModel):
    address: Optional[str] = None
    latitude: float
    longitude: float
    city: Optional[str] = None
    state: Optional[str] = None
    country: str
    country_code: str


class LatLng(BaseModel):
    latitude: float
    longitude: float


def dms_to_location(
    GPSLatitudeRef: str,
    GPSLatitude: Tuple[float, float, float],
    GPSLongitudeRef: str,
    GPSLongitude: Tuple[float, float, float],
) -> Location:
    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    location = reverse_geo_code(latlng.latitude, latlng.longitude)

    return location


def dms_to_degrees(
    GPSLatitudeRef: str,
    GPSLatitude: Tuple[float, float, float],
    GPSLongitudeRef: str,
    GPSLongitude: Tuple[float, float, float],
) -> LatLng:
    lat_sign = -1 if GPSLatitudeRef == "S" else 1
    lng_sign = -1 if GPSLongitudeRef == "W" else 1

    latitude = lat_sign * (GPSLatitude[0] + GPSLatitude[1] / 60 + GPSLatitude[2] / 3600)
    longitude = lng_sign * (
        GPSLongitude[0] + GPSLongitude[1] / 60 + GPSLongitude[2] / 3600
    )

    return LatLng(latitude=latitude, longitude=longitude)


def reverse_geo_code(lat: float, lng: float) -> Location:
    try:
        rev = reverse((lat, lng), language="en")

        rev_address = rev.raw.get("address")

        log.info(f"Reverse geocoding: {lat}, {lng}.")
        return Location(
            **{
                "address": rev.address,
                "latitude": lat,
                "longitude": lng,
                "city": rev_address.get("city") if rev_address is not None else None,
                "state": rev_address.get("state") if rev_address is not None else None,
                "country": rev_address.get("country")
                if rev_address is not None
                else None,
                "country_code": rev_address.get("country_code")
                if rev_address is not None
                else None,
            }
        )
    except Exception as e:
        log.error(f"Failed to reverse geocode: {lat}, {lng}. Exception: {e}.")
        return {
            "address": None,
            "latitude": None,
            "longitude": None,
            "city": None,
            "state": None,
            "country": None,
            "country_code": None,
        }
