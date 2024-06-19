from typing import Literal
from pydantic import BaseModel, RootModel
from dataclasses import dataclass
from pure_cv import Rotation
from moveread.boxes import Rectangle
from moveread.annotations import ImageMeta, Corners


class ImageResult(BaseModel):
  img: str
  meta: ImageMeta

class Result(BaseModel):
  original: ImageResult
  corrected: ImageResult
  boxes: list[str]

@dataclass
class Discarded:
  reason: Literal['manually-discarded'] = 'manually-discarded'

class BaseInput(BaseModel):
  img: str
  model: str
  blobs: list[str] = []

  def correct(self, corners: Corners, corrected: str, confirmed: bool = True) -> 'Corrected':
    return Corrected(blobs=self.blobs + [corrected], img=self.img, model=self.model, corners=corners, corrected=corrected, confirmed=confirmed)
  
  def rotate(self, rotation: Rotation, rotated: str) -> 'Rotated':
    return Rotated(blobs=self.blobs + [rotated], img=rotated, model=self.model, rotation=rotation)
    
  def extract(self, corrected: str, contours, contoured: str) -> 'Extracted':
    return Extracted(blobs=self.blobs + [contoured, corrected], img=self.img, model=self.model, corrected=corrected, confirmed=False, contours=contours, contoured=contoured)
  
class Input(BaseInput):
  tag: Literal['input'] = 'input'

class Corrected(BaseInput):
  corners: Corners | None = None
  corrected: str
  confirmed: bool

  def select(self, grid_coords: Rectangle) -> 'Selected':
    return Selected(blobs=self.blobs, img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed, grid_coords=grid_coords)
  
  def re_extract(self, contours, contoured: str) -> 'Extracted':
    return Extracted(blobs=self.blobs + [contoured], img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed, contours=contours, contoured=contoured)

class Rotated(Input):
  rotation: Rotation

class Extracted(Corrected):
  contours: list
  contoured: str

  def ok(self) -> 'Contoured':
    return Contoured(blobs=self.blobs, img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed, contours=self.contours, contoured=self.contoured)

  def perspective_ok(self) -> 'Corrected':
    return Corrected(blobs=self.blobs, img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed)

class Selected(Corrected):
  grid_coords: Rectangle
  tag: Literal['grid'] = 'grid'

class Contoured(Extracted):
  tag: Literal['contoured'] = 'contoured'

Output = Selected | Contoured
class PreOutput(RootModel):
  root: Output

class Validate(Extracted):
  tag: Literal['validate'] = 'validate'
  @classmethod
  def of(cls, extracted: Extracted):
    return Validate(img=extracted.img, model=extracted.model, blobs=extracted.blobs, corners=extracted.corners, corrected=extracted.corrected, confirmed=extracted.confirmed, contours=extracted.contours, contoured=extracted.contoured)

class Correct(BaseInput):
  tag: Literal['correct'] = 'correct'
  @classmethod
  def of(cls, input: BaseInput):
    return Correct(img=input.img, model=input.model, blobs=input.blobs)

class Reextract(Corrected):
  tag: Literal['reextract'] = 'reextract'
  @classmethod
  def of(cls, corrected: Corrected):
    return Reextract(img=corrected.img, model=corrected.model, blobs=corrected.blobs, corners=corrected.corners, corrected=corrected.corrected, confirmed=corrected.confirmed)

class Revalidate(Extracted):
  tag: Literal['revalidate'] = 'revalidate'
  @classmethod
  def of(cls, extracted: Extracted):
    return Revalidate(img=extracted.img, model=extracted.model, blobs=extracted.blobs, corners=extracted.corners, corrected=extracted.corrected, confirmed=extracted.confirmed, contours=extracted.contours, contoured=extracted.contoured)

class Select(Corrected):
  tag: Literal['select'] = 'select'
  @classmethod
  def of(cls, corrected: Corrected):
    return Select(img=corrected.img, model=corrected.model, blobs=corrected.blobs, corners=corrected.corners, corrected=corrected.corrected, confirmed=corrected.confirmed)

__all__ = [
  'Discarded', 'BaseInput', 'Corrected', 'Rotated', 'Extracted', 'Selected', 'Contoured', 'Output',
  'ImageResult', 'Result',
  'Validate', 'Correct', 'Reextract', 'Revalidate', 'Select', 'PreOutput',
]
