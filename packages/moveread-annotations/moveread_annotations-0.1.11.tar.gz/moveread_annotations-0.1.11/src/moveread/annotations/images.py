from typing import Literal, NamedTuple
from pydantic import ConfigDict
from moveread.boxes import Annotations as ImageAnnotations

Source = Literal['raw-scan', 'corrected-scan', 'camera', 'corrected-camera', 'robust-corrected'] 

Vec2 = tuple[float, float]

class Corners(NamedTuple):
  tl: Vec2
  tr: Vec2
  br: Vec2
  bl: Vec2

class ImageMeta(ImageAnnotations):
  model_config = ConfigDict(extra='allow')
  source: Source | None = None
  perspective_corners: Corners | None = None
