from fastapi import FastAPI
from api.study_router import router as study_router

app = FastAPI(
    title="Toxicology Meta-Agent API",
    description="API multiagente para avaliação de dados pré-clínicos",
    version="0.1.0"
)

app.include_router(study_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
