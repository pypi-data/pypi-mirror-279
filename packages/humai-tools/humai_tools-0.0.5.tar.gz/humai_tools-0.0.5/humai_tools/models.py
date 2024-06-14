from pydantic import BaseModel
from typing import List, Optional
import datetime


class Choice(BaseModel):
    question: str
    answers: List[str]
    correct: int
    time: int  # tiempo para la pregunta en kahoot


class Quiz(BaseModel):
    items: List[Choice]


class Cell(BaseModel):
    type: str
    content: str


class Notebook(BaseModel):
    name: str
    cells: List[Cell]
    nb_json: str
    filename: str
    category: Optional[str]  # solutions, exercises, base


class Class(BaseModel):
    name: str
    short_description: Optional[str]
    long_description: Optional[str]
    quiz: Optional[Quiz]
    scheduled_date: Optional[datetime.datetime]
    ipynbs: Optional[List[Notebook]]  # link de drive, o ipynb o pptx?
    video_urls: Optional[List[str]]  # link videos youtube


class Course(BaseModel):
    name: str
    classes: List[Class]
    readme: Optional[str]
