from typing_extensions import TypedDict, NotRequired, Unpack, Annotated
import numpy as np
import cv2 as cv
from scoresheet_models import Model
from .annotations import Rectangle, Vec2

class Pads(TypedDict):
  l: float
  r: float
  t: float
  b: float

class Params(TypedDict):
  coords: Rectangle
  model: Model
  pads: NotRequired[Pads|None]

default_pads = Pads(l=0.1, r=0.1, t=0.2, b=0.2)

def absolute_positions(img_width: int, img_height: int, rect: Rectangle, model: Model) -> list[Vec2]:
  """Box positions as defined by `rect` scaled to `img_size`"""
  tl = np.array(rect['tl']) * [img_width, img_height]
  size = np.array(rect['size']) * [img_width, img_height]
  return model.box_positions * size + tl # type: ignore

def padded_rois(tl: Annotated[np.ndarray, "N 2"], size: Vec2, pads: Pads = default_pads) -> Annotated[np.ndarray, "N 4"]:
  """Returns `l, r, t, b` coords of ROIs
  - `tl`: array of top-left positions (shape `N x 2`)
  - `size`: ROI size
  - `pads`: relative paddings (relative to `size`)
  """
  p = default_pads | pads
  pads_array = np.array([p['l'], p['r'], p['t'], p['b']])
  lrtb = np.zeros((tl.shape[0], 4))
  lrtb[:, 0] = tl[:, 0] - pads_array[0] * size[0]
  lrtb[:, 1] = tl[:, 0] + (1 + pads_array[1]) * size[0]
  lrtb[:, 2] = tl[:, 1] - pads_array[2] * size[1]
  lrtb[:, 3] = tl[:, 1] + (1 + pads_array[3]) * size[1]
  return np.round(lrtb).astype(int).clip(0)

def box_positions(img: cv.Mat, **p: Unpack[Params]) -> list[Vec2]:
  return absolute_positions(img.shape[1], img.shape[0], p['coords'], p['model'])

def extract_grid(img: cv.Mat, **p: Unpack[Params]) -> list[cv.Mat]:
  """Extract boxes from `img`"""
  imh, imw = img.shape[:2]
  positions = box_positions(img, **p)
  box_size = np.array(p['model'].box_size) * [imw, imh] * p['coords']['size']
  rois = padded_rois(positions, box_size, p.get('pads') or {}) # type: ignore
  return [img[t:b, l:r] for l, r, t, b in rois] # type: ignore
