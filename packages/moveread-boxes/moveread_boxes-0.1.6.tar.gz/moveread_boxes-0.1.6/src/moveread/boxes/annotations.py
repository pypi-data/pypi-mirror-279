from typing import Literal
from typing_extensions import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel
from haskellian import Either, Left, Right
from scoresheet_models import ModelID
from robust_extraction import Contours

Vec2 = tuple[float, float]

class Rectangle(TypedDict):
  tl: Vec2
  size: Vec2

class Annotations(BaseModel):
  grid_coords: Rectangle | None = None
  """Grid coords (matching some scoresheet model)"""
  box_contours: Contours | None = None
  """Explicit box contours (given by robust-extraction, probably)"""

class ExportableGrid(BaseModel):
  tag: Literal['grid'] = 'grid'
  grid_coords: Rectangle
  model: ModelID

class ExportableContours(BaseModel):
  tag: Literal['contours'] = 'contours'
  box_contours: Contours

ExportableAnnotations = ExportableGrid | ExportableContours

@dataclass
class MissingMeta:
  detail: str
  reason: Literal['missing-metadata'] = 'missing-metadata'

def exportable(ann: Annotations, model: ModelID | None = None) -> Either[MissingMeta, ExportableAnnotations]:
  """Make exportable metadata if possible"""
  if ann.box_contours is not None:
    return Right(ExportableContours(box_contours=ann.box_contours))
  if ann.grid_coords is None:
    return Left(MissingMeta('No `box_contours` nor `grid_coords` provided'))
  if model is None:
    return Left(MissingMeta('Model parameter required when relying on `grid_coords`'))
  return Right(ExportableGrid(grid_coords=ann.grid_coords, model=model))