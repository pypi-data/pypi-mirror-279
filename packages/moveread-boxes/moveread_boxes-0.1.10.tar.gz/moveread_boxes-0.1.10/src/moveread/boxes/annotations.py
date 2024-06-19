from typing import Literal
from typing_extensions import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel, SkipValidation
from haskellian import Either, Left, Right
from jaxtyping import Int
from py_jaxtyping import PyArray

Contours = PyArray[Int, int, 'N 4 1 2']

Vec2 = tuple[float, float]

class Rectangle(TypedDict):
  tl: Vec2
  size: Vec2

class Annotations(BaseModel):
  grid_coords: Rectangle | None = None
  """Grid coords (matching some scoresheet model)"""
  box_contours: SkipValidation[Contours | None] = None
  """Explicit box contours (given by robust-extraction, probably)"""

class ExportableGrid(BaseModel):
  tag: Literal['grid'] = 'grid'
  grid_coords: Rectangle
  model: str

class ExportableContours(BaseModel):
  tag: Literal['contours'] = 'contours'
  box_contours: SkipValidation[Contours]

ExportableAnnotations = ExportableGrid | ExportableContours

@dataclass
class MissingMeta:
  detail: str
  reason: Literal['missing-metadata'] = 'missing-metadata'

def exportable(ann: Annotations, model: str | None = None) -> Either[MissingMeta, ExportableAnnotations]:
  """Make exportable metadata if possible"""
  if ann.box_contours is not None:
    return Right(ExportableContours(box_contours=ann.box_contours))
  if ann.grid_coords is None:
    return Left(MissingMeta('No `box_contours` nor `grid_coords` provided'))
  if model is None:
    return Left(MissingMeta('Model parameter required when relying on `grid_coords`'))
  return Right(ExportableGrid(grid_coords=ann.grid_coords, model=model))