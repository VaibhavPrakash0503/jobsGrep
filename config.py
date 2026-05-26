from dotenv import load_dotenv
import os

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


class Config:
    # Search
    keywords = [
        "backend intern",
        "fullstack intern",
        "devops intern",
        "backend developer intern",
        "fullstack developer intern",
        "software intern python",
        "software intern golang",
        "software intern node",
        "backend fresher",
        "devops fresher",
    ]

    location = "India"
    hours_old = 13
    results_per_site = 20
    sites = ["indeed", "linkedin"]

    # Role filter — only these roles allowed
    allowed_roles = [
        "backend",
        "full stack",
        "fullstack",
        "full-stack",
        "devops",
        "software",
        "platform",
        "infrastructure",
        "site reliability",
        "sre",
        "cloud",
    ]

    # Tech stack filter
    allowed_stack = [
        "python",
        "go",
        "golang",
        "javascript",
        "js",
        "node",
        "node.js",
        "nodejs",
        "typescript",
        "docker",
        "kubernetes",
        "redis",
        "aws",
        "linux",
    ]

    # Location filter
    # allowed_locations = ["remote", "work from home", "wfh"]

    # Exclude these companies (service based)
    exclude_companies = [
        "tcs",
        "infosys",
        "wipro",
        "cognizant",
        "accenture",
        "capgemini",
        "hcl",
        "tech mahindra",
        "mphasis",
    ]

    # Fresher signals
    experience_keywords = [
        "fresher",
        "entry level",
        "0-1 years",
        "0-2 years",
        "intern",
        "trainee",
        "graduate",
        "no experience",
        "fresh graduate",
    ]

    # Exclude senior roles
    exclude_keywords = [
        "senior",
        "lead",
        "manager",
        "architect",
        "principal",
        "5+ years",
        "7+ years",
        "10+ years",
        "staff engineer",
    ]
    # Telegram
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Database
    db_path = "data/jobs.db"
