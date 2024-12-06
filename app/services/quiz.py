import json
from typing import List, Optional
from pathlib import Path
from app.models.quiz import Quiz, Question

QUIZ_FILE = Path(__file__).resolve().parent.parent / "data" / "quizzes.json"

def load_quizzes() -> List[Quiz]:
    """
    Load all quizzes from the quizzes.json file.
    Returns a list of Quiz objects.
    """
    if not QUIZ_FILE.exists():
        raise FileNotFoundError(f"Quiz file not found at {QUIZ_FILE}")
    
    try:
        with open(QUIZ_FILE, "r", encoding="utf-8") as f:
            quizzes_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")
    
    quizzes = []
    for quiz_data in quizzes_data:
        try:
            questions = [
                Question(**question) for question in quiz_data["questions"]
            ]
            quizzes.append(
                Quiz(
                    id=quiz_data["id"],
                    title=quiz_data["title"],
                    duration=quiz_data["duration"],
                    difficulty=quiz_data["difficulty"],
                    questions=questions,
                )
            )
        except KeyError as e:
            raise ValueError(f"Missing key in quiz data: {e}")
    return quizzes

def get_quiz_by_id(quiz_id: int) -> Optional[Quiz]:
    """
    Get a quiz by its ID.
    """
    quizzes = load_quizzes()
    for quiz in quizzes:
        if quiz.id == quiz_id:
            return quiz
    return None

def calculate_score(quiz: Quiz, answers: List[int]) -> int:
    """
    Calculate the score based on the provided answers.
    """
    score = 0
    for question, user_answer in zip(quiz.questions, answers):
        if question.index_correct_option == user_answer:
            score += question.mark
    return score
