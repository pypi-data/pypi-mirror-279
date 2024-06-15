from exiffusion.geo import dms_to_degrees
from exiffusion.geo import reverse_geo_code
from exiffusion.geo import dms_to_location


def test_dms_to_location_europe():
    GPSLatitudeRef = "N"
    GPSLatitude = (46.0, 28.0, 15.79)
    GPSLongitudeRef = "E"
    GPSLongitude = (30.0, 44.0, 28.3)

    location = dms_to_location(
        GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude
    )

    assert location.city == "Odesa"


def test_dms_to_location_south_america():
    GPSLatitudeRef = "S"
    GPSLatitude = (33.0, 26.0, 50.9532)
    GPSLongitudeRef = "W"
    GPSLongitude = (70.0, 40.0, 25.2336)

    location = dms_to_location(
        GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude
    )

    assert location.city == "Santiago"


def test_dms_to_degrees_europe():
    GPSLatitudeRef = "N"
    GPSLatitude = (46.0, 28.0, 15.79)
    GPSLongitudeRef = "E"
    GPSLongitude = (30.0, 44.0, 28.3)

    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    assert round(latlng.latitude, 6) == 46.471053
    assert round(latlng.longitude, 6) == 30.741194


def test_dms_to_degrees_asia():
    GPSLatitudeRef = "N"
    GPSLatitude = (35.0, 39.0, 10.1952)
    GPSLongitudeRef = "E"
    GPSLongitude = (139.0, 50.0, 22.1208)

    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    assert round(latlng.latitude, 6) == 35.652832
    assert round(latlng.longitude, 6) == 139.839478


def test_dms_to_degrees_north_america():
    GPSLatitudeRef = "N"
    GPSLatitude = (43.0, 39.0, 3.852)
    GPSLongitudeRef = "W"
    GPSLongitude = (79.0, 20.0, 49.254)

    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    assert round(latlng.latitude, 6) == 43.651070
    assert round(latlng.longitude, 6) == -79.347015


def test_dms_to_degrees_south_america():
    GPSLatitudeRef = "S"
    GPSLatitude = (33.0, 26.0, 50.9532)
    GPSLongitudeRef = "W"
    GPSLongitude = (70.0, 40.0, 25.2336)

    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    assert round(latlng.latitude, 6) == -33.447487
    assert round(latlng.longitude, 6) == -70.673676


def test_dms_to_degrees_south_oceania():
    GPSLatitudeRef = "S"
    GPSLatitude = (33.0, 51.0, 54.5148)
    GPSLongitudeRef = "E"
    GPSLongitude = (151.0, 12.0, 35.64)

    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    assert round(latlng.latitude, 6) == -33.865143
    assert round(latlng.longitude, 6) == 151.209900


def test_reverse_geo_code():
    location = reverse_geo_code(51.5073219, -0.1276474)
    assert location.latitude == 51.5073219
    assert location.longitude == -0.1276474
    assert location.city == "City of Westminster"
    assert location.state == "England"
    assert location.country == "United Kingdom"
    assert location.country_code == "gb"


def test_reverse_geo_code_missing_city():
    location = reverse_geo_code(51.894525, -116.682883)
    assert location.latitude == 51.894525
    assert location.longitude == -116.682883
    assert location.city is None
    assert location.state == "Alberta"
    assert location.country == "Canada"
    assert location.country_code == "ca"
    assert location.address.split(",")[0] == "Balfour Wall Route"
