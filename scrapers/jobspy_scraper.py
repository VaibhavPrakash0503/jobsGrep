import pandas as pd
import logging
from jobspy import scrape_jobs
from config import Config

logger = logging.getLogger(__name__)


def scrape() -> list[dict]:
    all_jobs = []

    for keyword in Config.keywords:
        try:
            jobs: pd.DataFrame = scrape_jobs(
                site_name=Config.sites,
                search_term=keyword,
                location=Config.location,
                hours_old=Config.hours_old,
                results_per_site=Config.results_per_site,
                country_indeed="India",
                is_remote=True,
            )

            if jobs.empty:
                continue

            for _, row in jobs.iterrows():
                all_jobs.append(
                    {
                        "id": str(row.get("id", "")),
                        "title": str(row.get("title", "")),
                        "company": str(row.get("company", "")),
                        "location": str(row.get("location", "")),
                        "url": str(row.get("job_url", "")),
                        "description": str(row.get("description", ""))[:500],
                        "date_posted": str(row.get("date_posted", "")),
                        "source": str(row.get("site", "")),
                    }
                )

        except Exception as e:
            logger.warning(f"[JobSpy] Error scraping '{keyword}': {e}")
            continue

    seen_urls = set()
    unique_jobs = []
    for job in all_jobs:
        if job["url"] not in seen_urls:
            unique_jobs.append(job)
            seen_urls.add(job["url"])

    logger.info(
        f"[JobSpy] Scraped {len(unique_jobs)} unique jobs for keywords: {Config.keywords}"
    )
    return unique_jobs
