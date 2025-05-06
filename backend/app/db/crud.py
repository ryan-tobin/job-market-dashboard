from sqlalchemy.orm import Session 
from app.db.models import Job 

def create_job(db:Session, job_data: dict):
    existing = db.query(Job).filter_by(
        title=job_data['title'],company=job_data['company']
    ).first()

    if existing:
        return existing
    
    new_job = Job(
        title=job_data['title'],
        company=job_data['company'],
        location=job_data["location"],
        tags=','.join(job_data['tags'])
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job