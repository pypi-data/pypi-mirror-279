from typing import Literal
from pydantic import BaseModel
from moveread.boxes import Rectangle

class Task(BaseModel):
  img: str
  model: str

class Selected(BaseModel):
  tag: Literal['selected'] = 'selected'
  grid_coords: Rectangle

class Recorrect(BaseModel):
  tag: Literal['recorrect'] = 'recorrect'

Result = Selected | Recorrect