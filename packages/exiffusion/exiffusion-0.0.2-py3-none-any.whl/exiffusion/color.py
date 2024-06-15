from pydantic import BaseModel


class Color(BaseModel):
    R: int
    G: int
    B: int


def color_contrast(color_a: Color, color_b: Color):
    # Following Chromium's implementation of the color-contrast function specified in the W3C web standards.
    #
    # Reference:
    # https://issues.chromium.org/issues/40142548
    # https://ux.stackexchange.com/questions/82056/how-to-measure-the-contrast-between-any-given-color-and-white/82068#82068
    # https://github.com/chromium/chromium/blob/main/third_party/blink/renderer/core/css/properties/css_parsing_utils.cc#L2345
    # https://github.com/chromium/chromium/blob/main/ui/gfx/color_utils.cc#L400
    # https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef

    lum_a = get_relative_luminance(color_a)
    lum_b = get_relative_luminance(color_b)

    return get_contrast_ratio(lum_a, lum_b)


def get_contrast_ratio(luminance_a: float, luminance_b: float):
    luminance_a += 0.05
    luminance_b += 0.05

    if luminance_a > luminance_b:
        return luminance_a / luminance_b
    else:
        return luminance_b / luminance_a


def get_relative_luminance(color: Color):
    return (
        (0.2126 * linearize(color.R))
        + (0.7152 * linearize(color.G))
        + (0.0722 * linearize(color.B))
    )


def linearize(component: float):
    # https://github.com/chromium/chromium/blob/main/ui/gfx/color_utils.cc#L63
    # https://en.wikipedia.org/wiki/SRGB#Computing_the_transfer_function

    component = component / 255

    if component <= 0.04045:
        return component / 12.92
    else:
        return ((component + 0.055) / 1.055) ** 2.4
