from pydantic import BaseModel
from typing import List, Optional

class QuestionSchema(BaseModel):
    text: str
    options: List[str]
    index_correct_option: int
    mark: int

class QuizSchema(BaseModel):
    id: int
    title: str
    duration: int  # in seconds
    difficulty: str
    questions: List[QuestionSchema]

class AnswerSchema(BaseModel):
    quiz_id: int
    answers: List[int]  # list of the answers for the questions
