# Moveread Boxes

> Annotating and exporting boxes

## Usage

```python
import cv2 as cv
from scoresheet_models import models
import moveread.boxes as bxs
```

### Grid Extraction

```python
ann = bxs.exportable(
  bxs.Annotations(grid_coords=bxs.Rectangle(tl=(0.05, 0.195), size=(0.935, 0.66))),
  'fcde'
).unsafe()
boxes = bxs.export(fcde_sheet, ann)
# [cv.Mat(...), ...]

bxs.exportable(sheet, ann)
# Left(value=MissingAnnotations(detail='Model parameter required when relying on `grid_coords`'))

bxs.exportable(sheet, ann=Annotations())
# Left(value=MissingAnnotations(detail='No `grid_coords` provided'))
```

### Contour Extraction

```python
import robust_extraction as re

model = 'llobregat23'
res = re.descaled_extract(sheet, model)
ann = bxs.exportable(bxs.Annotations(box_contours=res.contours), model).unsafe()
boxes = bxs.export(res.corr_img, ann)
```