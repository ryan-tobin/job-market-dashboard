from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import jobs
from app.db.database import Base, engine 
from app.db import models
from app.tasks.scheduler import start_scheduler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"message": "Welcome to the Job Market API"}

app.include_router(jobs.router, prefix="/api/jobs")

def init_db():
    Base.metadata.create_all(bind=engine)

init_db()
