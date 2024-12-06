from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    text: str
    options: List[str]
    index_correct_option: int
    mark: int

class Quiz(BaseModel):
    id: int
    title: str
    duration: int  # in seconds
    difficulty: str
    questions: List[Question]
