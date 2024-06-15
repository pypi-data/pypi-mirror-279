from . import EXAMPLE_SOURCE_DIR

from exiffusion.exif import get_exif


def test_get_exif():
    img = EXAMPLE_SOURCE_DIR / "odesa.HEIC"
    exif_data = get_exif(img)

    assert exif_data.Orientation == 1
    assert exif_data.DateTime == "2023:09:25 16:29:37"
    assert exif_data.GPSLatitudeRef == "N"
    assert exif_data.GPSLatitude == (46.0, 28.0, 15.79)
    assert exif_data.GPSLongitudeRef == "E"
    assert exif_data.GPSLongitude == (30.0, 44.0, 28.3)


def test_get_exif_detailed_tags():
    img = EXAMPLE_SOURCE_DIR / "odesa.HEIC"
    exif_data = get_exif(img, get_detailed_tags=True)

    assert exif_data.Orientation == 1
    assert exif_data.DateTime == "2023:09:25 16:29:37"
    assert exif_data.Make == "Apple"
    assert exif_data.Model == "iPhone 12 Pro Max"
    assert exif_data.HostComputer == "iPhone 12 Pro Max"
    assert exif_data.Software == "16.6.1"
    assert exif_data.GPSLatitudeRef == "N"
    assert exif_data.GPSLatitude == (46.0, 28.0, 15.79)
    assert exif_data.GPSLongitudeRef == "E"
    assert exif_data.GPSLongitude == (30.0, 44.0, 28.3)
    assert exif_data.ShutterSpeedValue == 8.467022820208415
    assert exif_data.ApertureValue == 1.3561438092556088
    assert exif_data.DateTimeOriginal == "2023:09:25 16:29:37"
    assert exif_data.DateTimeDigitized == "2023:09:25 16:29:37"
    assert exif_data.BrightnessValue == 6.513317043372022
    assert exif_data.ExposureBiasValue == 0.0
    assert exif_data.MeteringMode == 5
    assert exif_data.ColorSpace == 65535
    assert exif_data.Flash == 16
    assert exif_data.FocalLength == 5.1
    assert exif_data.ExifImageWidth == 4032
    assert exif_data.ExifImageHeight == 3024
    assert exif_data.FocalLengthIn35mmFilm == 26
    assert exif_data.OffsetTime == "+03:00"
    assert exif_data.SubsecTimeOriginal == "229"
    assert exif_data.SubjectLocation == (2002, 1503, 2213, 1327)
    assert exif_data.SubsecTimeDigitized == "229"
    assert exif_data.SensingMethod == 2
    assert exif_data.ExposureTime == 0.002824858757062147
    assert exif_data.WhiteBalance == 0
    assert exif_data.LensSpecification == (1.5399999618512084, 7.5, 1.6, 2.4)
    assert exif_data.LensMake == "Apple"
    assert exif_data.LensModel == "iPhone 12 Pro Max back triple camera 5.1mm f/1.6"
    assert exif_data.CompositeImage == 2
