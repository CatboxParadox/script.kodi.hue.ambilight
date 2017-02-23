import image
import pytest


def test_hsvratio_init():
    ratio = image.HSVRatio()

    assert ratio.h == 0.0
    assert ratio.s == 0.0
    assert ratio.v == 0.0
    assert ratio.ratio == 0.0


def test_hsvratio_init_params():
    ratio = image.HSVRatio(hue=15.2, saturation=99.1, value=54.3, ratio=1.0)

    assert ratio.h == 15.2
    assert ratio.s == 99.1
    assert ratio.v == 54.3
    assert ratio.ratio == 1.0


RATIO_AVERAGE_TEST_DATA = [
    (15.2, 99.1, 54.3, 1.0,  13.9, 0.2, 19.5, 14.55, 49.65, 36.9, 1.0),
    (32, 0, 0, 0, 32, 0, 0, 32, 0, 0, 0),
    (15, 0, 0, 0, 16, 0, 0, 15, 0, 0, 0),
    (0, 32, 0, 0, 0, 32, 0, 0, 32, 0, 0),
    (0, 16, 0, 0, 0, 15, 0, 0, 15, 0, 0),
    (0, 0, 32, 0, 0, 0, 32, 0, 0, 32, 0),
    (0, 0, 15, 0, 0, 0, 16, 0, 0, 15, 0),
]


@pytest.mark.parametrize("h,s,v,ratio,th,ts,tv,eh,es,ev,eratio",
                         RATIO_AVERAGE_TEST_DATA)
def test_hsvratio_average(h, s, v, ratio, th, ts, tv, eh, es, ev, eratio):
    r = image.HSVRatio(hue=h, saturation=s, value=v, ratio=ratio)

    r.average(th, ts, tv)

    assert r.h == eh
    assert r.s == es
    assert r.v == ev
    assert r.ratio == eratio


RATIO_AVERAGE_VALUE_TEST_DATA = [
    (15.2, 99.1, 54.3, 0, 125.3, 89.8),
    (15.2, 99.1, 54.3, 0.5, 125.3, 89.8),
    (15.2, 99.1, 54.3, 0.51, 125.3, 89.09),
    (15.2, 99.1, 54.3, 1, 125.3, 54.3),
]


@pytest.mark.parametrize("h,s,v,ratio,val,expected",
                         RATIO_AVERAGE_VALUE_TEST_DATA)
def test_hsvratio_average_value(h, s, v, ratio, val, expected):
    r = image.HSVRatio(hue=h, saturation=s, value=v, ratio=ratio)
    r.averageValue(val)
    assert r.h == h
    assert r.s == s
    assert r.v == expected
    assert r.ratio == ratio


RATIO_HUE_TEST_DATA = [
    (1, 0.5, 80, 1.0, False, 0, 255, (65535, 127, 255)),
    (0.8, 0.9, 1.1, 1.0, False, 0, 255, (52428, 229, 255)),
    (0.8, 0.9, -0.5, 1.0, False, 0, 255, (52428, 229, 0)),
    (0.18, 0.5, 0.7, 1.0, True, 0, 255, (11796, 127, 178)),
    (0.19, 0.5, 0.6, 1.0, True, 0, 255, (12451, 127, 153)),
    (0.065, 0.5, 1.2, 1.0, True, 0, 255, (4259, 127, 255)),
    (0.4, 0.9, 0.5, 1.0, True, 0, 255, (26214, 229, 127)),
    (0.8, 0.9, 2, 1.0, True, 0, 255, (52428, 229, 255)),
]


@pytest.mark.parametrize("h,s,v,ratio,fullspectrum,bri_min,bri_max,expected",
                         RATIO_HUE_TEST_DATA)
def test_hsvratio_hue(h, s, v, ratio, fullspectrum, bri_min, bri_max, expected):
    r = image.HSVRatio(hue=h, saturation=s, value=v, ratio=ratio)
    assert r.hue(fullspectrum, bri_min, bri_max) == expected


SCREENSHOT_TEST_DATA = [
    ([106, 77, 255, 0] * 1000, 32, 32, -1, -1, 18,
     ((0.9722222222222222,  0.6980392156862745, 0.625),
      (0.9722222222222222,  0.6980392156862745, 0.625),
      (0.9722222222222222,  0.6980392156862745, 0.625))),
    ([199, 77, 106, 0] * 900 + [255, 255, 255, 0] * 100, 32, 32, -1, -1, 18,
     ((0.7055555555555556,  0.6130653266331658, 0.3455392156862716),
      (0.7055555555555556,  0.6130653266331658, 0.3455392156862716),
      (0.0, 0.0, 0.6002941176470569))),
    ([199, 77, 106, 0] * 900 + [255, 255, 255, 0] * 100, 32, 32, -1, -1, 1,
     ((0.3527777777777778,  0.3065326633165829, 0.5453921568627431),
      (0.3527777777777778,  0.3065326633165829, 0.5453921568627431),
      (0.3527777777777778,  0.3065326633165829, 0.5453921568627431))),
    ([199, 77, 106, 0] * 333 + [12, 149, 58, 0] * 333 + [106, 77, 255] * 333, 32, 32, -1, -1, 18,
     ((0.275,  0.9194630872483223, 0.3883139824316286),
      (0.7055555555555556,  0.6130653266331658, 0.4863531981179031),
      (0.9722222222222222,  0.6980392156862745, 0.5961571196865305))),
]


@pytest.mark.parametrize(
    "pixels,width,height,threshold_bri,threshold_sat,color_bias,expected",
    SCREENSHOT_TEST_DATA)
def test_spectrum_hsv(pixels, width, height, threshold_bri, threshold_sat,
                      color_bias, expected):
    s = image.Screenshot(pixels, width, height)
    spectrum = s.spectrum_hsv(
        pixels, width, height, threshold_bri, threshold_sat, color_bias
    )
    for idx in range(3):
        print idx
        assert spectrum[idx].h == expected[idx][0]
        assert spectrum[idx].s == expected[idx][1]
        assert spectrum[idx].v == expected[idx][2]


def test_rgb_from_pixels():
    pixels = [123, 256, 129, 143, 32]
    assert image._rgb_from_pixels(pixels, 0, rgba=True) == [123, 256, 129]
    assert image._rgb_from_pixels(pixels, 0) == [129, 256, 123]
    assert (image._rgb_from_pixels(pixels, 1, rgba=True) ==
            [256, 129, 143] ==
            image._rgb_from_pixels(pixels, 1)[::-1])
