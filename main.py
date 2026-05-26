import asyncio
import logging
from scrapers.jobspy_scraper import scrape
from filters import filter_jobs
from db import init_db, filter_unseen, mark_seen
from notify import notify

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # terminal
        logging.FileHandler("data/jobbot.log"),  # log file
    ],
)

logger = logging.getLogger(__name__)


def run() -> None:
    logger.info("===== JobBot Started =====")

    # step 1 — init db
    init_db()

    # step 2 — scrape
    jobs = scrape()
    if not jobs:
        logger.info("No jobs found this run")
        return

    # step 3 — filter fresher/intern
    filtered_jobs = filter_jobs(jobs)
    if not filtered_jobs:
        logger.info("No jobs passed filters this run")
        return

    # step 4 — dedup against db
    new_jobs = filter_unseen(filtered_jobs)
    if not new_jobs:
        logger.info("No new jobs after dedup")
        return

    # step 5 — notify
    asyncio.run(notify(new_jobs))

    # step 6 — mark seen
    mark_seen(new_jobs)

    logger.info(f"===== JobBot Done — {len(new_jobs)} new jobs sent =====")


if __name__ == "__main__":
    run()
