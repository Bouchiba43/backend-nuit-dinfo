from fastapi import APIRouter, HTTPException
from typing import List
from app.models.quiz import Quiz
from app.schemas.quiz import AnswerSchema
from app.services.quiz import get_quiz_by_id, calculate_score
from app.services.llama_service import LLaMAService
from pydantic import BaseModel

router = APIRouter()
llama_service = LLaMAService()

@router.get("/quiz/{quiz_id}", response_model=Quiz)
async def get_quiz(quiz_id: int):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/quiz/{quiz_id}/answer", response_model=str)
async def answer_quiz(quiz_id: int, answer: AnswerSchema):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if len(answer.answers) != len(quiz.questions):
        raise HTTPException(status_code=400, detail="Invalid number of answers")
    
    score = calculate_score(quiz, answer.answers)
    correct = score == sum(question.mark for question in quiz.questions)
    feedback = llama_service.generate_feedback(correct, [q.index_correct_option for q in quiz.questions], answer.answers)
    return feedback

class ChatRequest(BaseModel):
    user_input: str

@router.post("/chat", response_model=str)
async def chat(chat_request: ChatRequest):
    user_input = chat_request.user_input
    response = llama_service.generate_response(user_input)
    return response
