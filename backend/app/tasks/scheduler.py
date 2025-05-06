from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.scraper import scrape_remoteok_json
from app.db.database import SessionLocal
from app.db import crud
import logging

logging.basicConfig(level=logging.INFO)

def scrape_and_store_jobs():
    logging.info('Running job scrape task...')
    db = SessionLocal()
    try:
        jobs = scrape_remoteok_json()
        for job in jobs:
            crud.create_job(db, job)
        logging.info(f"Saved {len(jobs)} jobs.")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_and_store_jobs, 'interval', minutes=60)
    scheduler.start()
