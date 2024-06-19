from typing import Literal, TypeGuard
from pydantic import BaseModel, ConfigDict
from moveread.annotations import Corners
from pure_cv import Rotation

class Task(BaseModel):
  img: str

class Corrected(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
  tag: Literal['corrected'] = 'corrected'
  corners: Corners

class Rotated(BaseModel):
  tag: Literal['rotated'] = 'rotated'
  rotation: Rotation

Result = Corrected | Rotated

def is_corrected(result: Result) -> TypeGuard[Corrected]:
  return result.tag == 'corrected'

def is_rotated(result: Result) -> TypeGuard[Rotated]:
  return result.tag == 'rotated'
