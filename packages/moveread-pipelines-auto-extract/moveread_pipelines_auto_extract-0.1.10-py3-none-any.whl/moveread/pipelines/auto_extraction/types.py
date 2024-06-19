from typing import Any
from pydantic import BaseModel, SkipValidation
from haskellian import Either
from jaxtyping import Int
from py_jaxtyping import PyArray

class Task(BaseModel):
  model: str
  img: bytes
  already_corrected: bool = False

class Ok(BaseModel):
  contours: SkipValidation[PyArray[Int, int, 'N 4 1 2']]
  corrected: bytes
  contoured: bytes

Result = Either[Any, Ok]