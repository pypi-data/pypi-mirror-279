from typing import Mapping
import numpy as np
from .annotations import ExportableAnnotations
import robust_extraction2 as re
import scoresheet_models as sm

def export(
  img: np.ndarray, ann: ExportableAnnotations,
  models: Mapping[str, sm.Model],
  pads: re.Pads = {}
) -> list[np.ndarray]:
  """Export an image's boxes"""
  if ann.tag == 'grid':
    return sm.extract_boxes(img, models[ann.model], **ann.grid_coords, pads=pads)
  else:
    return re.boxes(img=img, contours=ann.box_contours, **pads)