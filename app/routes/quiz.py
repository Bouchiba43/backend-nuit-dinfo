from fastapi import APIRouter, HTTPException
from typing import List
from app.models.quiz import Quiz
from app.schemas.quiz import AnswerSchema
from app.services.quiz import get_quiz_by_id, calculate_score

router = APIRouter()

@router.get("/quiz/{quiz_id}", response_model=Quiz)
async def get_quiz(quiz_id: int):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/quiz/{quiz_id}/answer", response_model=int)
async def answer_quiz(quiz_id: int, answer: AnswerSchema):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if len(answer.answers) != len(quiz.questions):
        raise HTTPException(status_code=400, detail="Invalid number of answers")
    
    score = calculate_score(quiz, answer.answers)
    return score

@router.post("/quiz/{quiz_id}/complete", response_model=int)
async def complete_quiz(quiz_id: int, answer: AnswerSchema):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if len(answer.answers) != len(quiz.questions):
        raise HTTPException(status_code=400, detail="Invalid number of answers")
    
    score = calculate_score(quiz, answer.answers)
    return score
