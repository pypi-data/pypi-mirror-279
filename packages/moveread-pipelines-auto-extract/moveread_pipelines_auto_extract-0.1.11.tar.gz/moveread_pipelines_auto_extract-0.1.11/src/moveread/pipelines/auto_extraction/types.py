from typing import Any
from pydantic import BaseModel
from haskellian import Either

class Task(BaseModel):
  model: str
  img: bytes
  already_corrected: bool = False

class Ok(BaseModel):
  contours: list
  corrected: bytes
  contoured: bytes

Result = Either[Any, Ok]