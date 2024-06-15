from importlib.resources import files
from pathlib import PosixPath
import logging

from PIL import ImageFont, ImageDraw, Image
from pillow_heif import register_heif_opener

from exiffusion.color import Color, color_contrast

register_heif_opener()

log = logging.getLogger(__name__)


def overlay_text(image: str | PosixPath, text: str, output_dir: str | PosixPath):
    log.info(f"Overlaying text on {image}.")
    img = Image.open(image)

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    text_color = calc_text_color(
        img,
        width - right - margin,
        height - bottom - margin,
        width - margin,
        height - margin,
    )

    draw.text(
        (width - right - margin, height - bottom - margin),
        text,
        (text_color.R, text_color.G, text_color.B),
        font=font,
    )

    output_name = image.name if type(image) is PosixPath else image.split("/")[-1]

    img.save(f"{output_dir}/{output_name}")


def calc_text_color(img: Image, left: int, top: int, right: int, bottom: int) -> Color:
    # 1. Calculate the dominant color of the text background
    # 2. Use a color_contrast function to select white or black

    log.info(f"Calculating text overlay color for {img.filename}.")

    cropped_img = img.crop([left, top, right, bottom])
    cropped_img.filename = img.filename
    dominant_color = calc_dominant_color(cropped_img)

    white = Color(R=255, G=255, B=255)
    black = Color(R=0, G=0, B=0)

    white_contrast = color_contrast(white, dominant_color)
    black_contrast = color_contrast(black, dominant_color)

    return white if white_contrast > black_contrast else black


def calc_dominant_color(img: Image, palette_size: int = 4) -> Color:
    # Reference
    # https://stackoverflow.com/a/61730849

    log.info(f"Calculating dominant color for text overlay region: {img.filename}.")

    # Reduce colors (uses k-means internally)
    paletted = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]

    log.info(
        f"Dominant color for text overlay region: {dominant_color}; {img.filename}"
    )
    return Color(R=dominant_color[0], G=dominant_color[1], B=dominant_color[2])
