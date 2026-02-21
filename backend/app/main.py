from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import document, query

app = FastAPI(title="RAG Document QA System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document.router)
app.include_router(query.router)

@app.get("/")
def root():
    return {"message": "RAG Document QA System is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}