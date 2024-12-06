from app.models.quiz import Quiz
from typing import List
from app.services.gpt_neo_service import GPTNeoService

gpt_service = GPTNeoService()

def generate_feedback(question, user_answer, is_correct):
    """
    Generate feedback for a question based on whether the user's answer was correct or not.
    """
    if is_correct:
        prompt = (
            f"The user answered correctly for the question: '{question.text}'. "
            f"Thank them warmly and explain why the answer '{question.options[user_answer]}' is correct in two sentences."
        )
    else:
        correct_answer = question.options[question.index_correct_option]
        prompt = (
            f"The user got the question wrong: '{question.text}'. "
            f"Correct them and explain why the correct answer is '{correct_answer}' in two sentences."
        )
    
    return gpt_service.generate_response(prompt)

def calculate_score_with_feedback(quiz: Quiz, answers: List[int]) -> dict:
    """
    Calculate the score and generate feedback for each question.
    """
    score = 0
    feedback = []
    correct_answers = []

    for question, user_answer in zip(quiz.questions, answers):
        is_correct = question.index_correct_option == user_answer
        correct_answers.append(is_correct)
        if is_correct:
            score += question.mark
        feedback.append(generate_feedback(question, user_answer, is_correct))
    
    return {"score": score, "feedback": feedback, "correct_answers": correct_answers}