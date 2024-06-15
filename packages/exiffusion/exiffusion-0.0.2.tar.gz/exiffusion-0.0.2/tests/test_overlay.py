from importlib.resources import files

from . import EXAMPLE_SOURCE_DIR

from exiffusion.overlay import calc_text_color, calc_dominant_color
from exiffusion.color import Color

from PIL import ImageFont, ImageDraw, Image
from pillow_heif import register_heif_opener

register_heif_opener()


def test_calc_text_color_odesa():
    img = Image.open(EXAMPLE_SOURCE_DIR / "odesa.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nOdesa, Ukraine"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    text_color = calc_text_color(
        img,
        width - right - margin,
        height - bottom - margin,
        width - margin,
        height - margin,
    )

    assert text_color == Color(R=0, G=0, B=0)


def test_calc_text_color_swapkopmund():
    img = Image.open(EXAMPLE_SOURCE_DIR / "swakopmund.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nSwakopmund, Namibia"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    text_color = calc_text_color(
        img,
        width - right - margin,
        height - bottom - margin,
        width - margin,
        height - margin,
    )

    assert text_color == Color(R=255, G=255, B=255)


def test_calc_text_color_dresden():
    img = Image.open(EXAMPLE_SOURCE_DIR / "dresden.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nDresden, Germany"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    text_color = calc_text_color(
        img,
        width - right - margin,
        height - bottom - margin,
        width - margin,
        height - margin,
    )

    assert text_color == Color(R=0, G=0, B=0)


def test_calc_text_color_poisson_blanc():
    img = Image.open(EXAMPLE_SOURCE_DIR / "poisson_blanc.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nPoisson Blanc, Canada"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    text_color = calc_text_color(
        img,
        width - right - margin,
        height - bottom - margin,
        width - margin,
        height - margin,
    )

    assert text_color == Color(R=255, G=255, B=255)


def test_calc_dominant_odesa():
    img = Image.open(EXAMPLE_SOURCE_DIR / "odesa.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nOdesa, Ukraine"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    cropped_img = img.crop(
        [
            width - right - margin,
            height - bottom - margin,
            width - margin,
            height - margin,
        ]
    )

    cropped_img.filename = img.filename

    dominant_color = calc_dominant_color(cropped_img)

    assert dominant_color == Color(R=220, G=207, B=184)


def test_calc_dominant_swakopmund():
    img = Image.open(EXAMPLE_SOURCE_DIR / "swakopmund.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nSwakopmund, Namibia"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    cropped_img = img.crop(
        [
            width - right - margin,
            height - bottom - margin,
            width - margin,
            height - margin,
        ]
    )

    cropped_img.filename = img.filename

    dominant_color = calc_dominant_color(cropped_img)

    assert dominant_color == Color(R=3, G=3, B=2)


def test_calc_dominant_dresden():
    img = Image.open(EXAMPLE_SOURCE_DIR / "dresden.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nDresden, Germany"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    cropped_img = img.crop(
        [
            width - right - margin,
            height - bottom - margin,
            width - margin,
            height - margin,
        ]
    )

    cropped_img.filename = img.filename

    dominant_color = calc_dominant_color(cropped_img)

    assert dominant_color == Color(R=182, G=183, B=182)


def test_calc_dominant_poisson_blanc():
    img = Image.open(EXAMPLE_SOURCE_DIR / "poisson_blanc.HEIC")

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    text = "2024-01-01 11:11:11\nPoisson Blanc, Canada"

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    cropped_img = img.crop(
        [
            width - right - margin,
            height - bottom - margin,
            width - margin,
            height - margin,
        ]
    )

    cropped_img.filename = img.filename

    dominant_color = calc_dominant_color(cropped_img)

    assert dominant_color == Color(R=2, G=2, B=2)
