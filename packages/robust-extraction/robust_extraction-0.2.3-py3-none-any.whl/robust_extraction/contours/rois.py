from typing import NamedTuple
import cv2 as cv
import ramda as R
from .types import Contour, Contours

class Pads(NamedTuple):
  l: float
  r: float
  t: float
  b: float

@R.curry
def roi(
  contour: Contour, img: cv.Mat,
  pads: Pads | None = None
) -> cv.Mat:
  """- `pads`: proportions of height/width to add as padding"""
  l, r, t, b = pads or (.1, .1, .15, .25)
  x, y, w, h = cv.boundingRect(contour)
  top = max(int(y - t*h), 0)
  bot = int(y + (1+b)*h)
  left = max(int(x - l*w), 0)
  right = int(x + (1+r)*w)
  return img[top:bot, left:right] # type: ignore


def extract_contours(
  img: cv.Mat, contours: Contours | list[Contour],
  *, pads: Pads | None = None
) -> list[cv.Mat]:
  return R.map(roi(img=img), contours, pads=pads) # type: ignore