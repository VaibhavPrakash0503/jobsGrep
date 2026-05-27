import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from config import Config
from db import init_db, filter_unseen, mark_seen, get_conn
from scrapers.jobspy_scraper import scrape
from filters import filter_jobs
from notify import notify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 <b>JobBot is running</b>\n\n"
        "Available commands:\n"
        "/search — search for new jobs\n"
        "/status — show DB stats\n"
        "/clear — clear seen jobs DB\n"
        "/help — show this message",
        parse_mode=ParseMode.HTML,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📖 <b>Commands</b>\n\n"
        "/search — run full pipeline\n"
        "/status — show last run stats\n"
        "/clear — reset seen jobs\n"
        "/help — show this message",
        parse_mode=ParseMode.HTML,
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔍 Searching for jobs, please wait...")

    try:
        await update.message.reply_text("📡 Scraping job sites...")
        jobs = scrape()

        if not jobs:
            await update.message.reply_text("😕 No jobs found this run")
            return

        await update.message.reply_text(f"⚙️ Filtering {len(jobs)} jobs...")
        filtered_jobs = filter_jobs(jobs)

        if not filtered_jobs:
            await update.message.reply_text("😕 No jobs passed filters")
            return

        new_jobs = filter_unseen(filtered_jobs)

        if not new_jobs:
            await update.message.reply_text("✅ No new jobs since last search")
            return

        await notify(new_jobs)
        mark_seen(new_jobs)

    except Exception as e:
        logger.error(f"[Bot] Search failed: {e}")
        await update.message.reply_text("❌ Error: Try again later")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        conn = get_conn()
        total = conn.execute("SELECT COUNT(*) FROM seen_jobs").fetchone()[0]
        latest = conn.execute(
            "SELECT seen_at FROM seen_jobs ORDER BY seen_at DESC LIMIT 1"
        ).fetchone()

        last_seen = latest[0] if latest else "Never"
        await update.message.reply_text(
            f"📊 <b>JobBot Status</b>\n\n"
            f"Total jobs seen: <b>{total}</b>\n"
            f"Last run: <b>{last_seen}</b>",
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching status: {e}")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        conn = get_conn()
        conn.execute("DELETE FROM seen_jobs")
        conn.commit()
        await update.message.reply_text(
            "🗑️ Cleared all seen jobs. Next /search will fetch fresh results."
        )
        logger.info("[Bot] DB cleared by user")
    except Exception as e:
        await update.message.reply_text(f"❌ Error clearing DB: {e}")


def main() -> None:
    init_db()
    app = Application.builder().token(Config.telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("clear", clear))

    logger.info("[Bot] JobBot started, listening for commands...")
    app.run_polling()


if __name__ == "__main__":
    main()
