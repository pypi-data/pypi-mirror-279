from exiffusion.color import get_relative_luminance
from exiffusion.color import get_contrast_ratio
from exiffusion.color import Color


def test_get_relative_luminance_white():
    white = Color(R=255, G=255, B=255)
    assert get_relative_luminance(white) == 1.0


def test_get_relative_luminance_black():
    black = Color(R=0, G=0, B=0)
    assert get_relative_luminance(black) == 0.0


def test_get_relative_luminance_orange():
    orange = Color(R=255, G=192, B=0)
    assert round(get_relative_luminance(orange), 2) == 0.590


def test_get_relative_luminance_pink():
    pink = Color(R=255, G=102, B=204)
    assert round(get_relative_luminance(pink), 2) == 0.350


def test_get_relative_luminance_blue():
    blue = Color(R=0, G=255, B=255)
    assert round(get_relative_luminance(blue), 2) == 0.790


def test_get_contrast_ratio_black_white():
    white = Color(R=255, G=255, B=255)
    black = Color(R=0, G=0, B=0)

    lum_black = get_relative_luminance(black)
    lum_white = get_relative_luminance(white)

    assert get_contrast_ratio(lum_black, lum_white) == 21.0


def test_get_contrast_ratio_black_pink():
    black = Color(R=0, G=0, B=0)
    pink = Color(R=255, G=102, B=204)

    lum_black = get_relative_luminance(black)
    lum_pink = get_relative_luminance(pink)

    assert round(get_contrast_ratio(lum_black, lum_pink), 2) == 8.02


def test_get_contrast_ratio_purple_green():
    purple = Color(R=129, G=37, B=162)
    green = Color(R=102, G=203, B=82)

    lum_purple = get_relative_luminance(purple)
    lum_green = get_relative_luminance(green)

    assert round(get_contrast_ratio(lum_purple, lum_green), 2) == 3.76
