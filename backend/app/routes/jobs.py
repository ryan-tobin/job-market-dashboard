from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from typing import List
from fastapi import Query

from app.db.database import SessionLocal
from app.db import crud 
from app.db.models import Job as JobModel
from app.models.job import Job as JobSchema
from app.utils.scraper import scrape_remoteok_json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/save")
def save_jobs(db: Session = Depends(get_db)):
    jobs = scrape_remoteok_json()
    saved = []
    for job in jobs:
        saved_job = crud.create_job(db, job)
        saved.append(saved_job)
    return {"saved_jobs": [j.title for j in saved]}

@router.get("/", response_model=List[JobSchema])
def get_jobs(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    location: str = Query(None),
    tag: str = Query(None)
):
    query = db.query(JobModel)

    if location:
        query = query.filter(JobModel.location.ilike(f"%{location}%"))
    if tag:
        query = query.filter(JobModel.tags.ilike(f"%{tag}%"))

    jobs = query.offset((page - 1) * limit).limit(limit).all()

    return [
        JobSchema(
            title=j.title,
            company=j.company,
            location=j.location,
            tags=j.tags.split(",")
        ) for j in jobs
    ]

@app.get('/health')
def health_check():
    return {"status": "ok"}
