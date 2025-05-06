import requests
import logging

def scrape_remoteok_json():
    try:
        response = requests.get("https://remoteok.com/remote-dev-jobs.json", headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()

        jobs = []
        for job in data[1:]:  # Skip the first item (metadata)
            jobs.append({
                "title": job.get("position") or job.get("title", "Unknown"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "Remote"),
                "tags": job.get("tags", []),
            })
        return jobs

    except Exception as e:
        logging.error(f"Scraper failed: {e}")
        return []