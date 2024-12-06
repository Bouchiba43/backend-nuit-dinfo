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
    answers: List[int]  # list of the user's answers to the questions
    feedback: Optional[List[str]] = None  # Feedback for each question
    correct_answers: Optional[List[bool]] = None  # Whether each answer was correct or not
