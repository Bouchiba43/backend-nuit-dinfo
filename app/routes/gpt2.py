from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.gpt2_service import GPT2Service

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

gpt2_service = GPT2Service()

@router.post("/generate")
async def generate_response(request: PromptRequest):
    try:
        response = gpt2_service.generate_response(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))