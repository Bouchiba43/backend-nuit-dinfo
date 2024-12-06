from fastapi import APIRouter, HTTPException
from app.schemas import AnswerSchema
from app.services.quiz import get_quiz_by_id, calculate_score_with_feedback
from app.services import gpt_service
from app.models.quiz import Quiz

router = APIRouter()

@router.get("/quiz/{quiz_id}", response_model=Quiz)
async def get_quiz(quiz_id: int):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/quiz/{quiz_id}/answer", response_model=dict)
async def answer_quiz(quiz_id: int, answer: AnswerSchema):
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if len(answer.answers) != len(quiz.questions):
        raise HTTPException(status_code=400, detail="Invalid number of answers")
    
    result = calculate_score_with_feedback(quiz, answer.answers)
    
    return result

def generate_feedback(question, user_answer, is_correct):
    """
    Generate feedback for a question based on whether the user's answer was correct or not.
    """
    if is_correct:
        prompt = (
            f"The user answered correctly for the question: '{question.text}'. "
            f"Thank them warmly and explain why the answer '{question.options[user_answer]}' is correct in one short sentence."
        )
    else:
        correct_answer = question.options[question.index_correct_option]
        prompt = (
            f"The user got the question wrong: '{question.text}'. "
            f"Correct them and explain why the correct answer is '{correct_answer}' in one short sentence."
        )
    
    return gpt_service.generate_response(prompt)
