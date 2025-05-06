from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    tags = Column(String)

    __table_args__ = (
        UniqueConstraint('title', 'company', 'location', name='uix_job_unique'),
    )
