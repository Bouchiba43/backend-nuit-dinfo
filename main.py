from fastapi import FastAPI
from app.routes import auth
from app.models.user import Base
from app.config import engine
from app.routes.quiz import router as quiz_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(quiz_router, prefix="/api", tags=["Quiz"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
