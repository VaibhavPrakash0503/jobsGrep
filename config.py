from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    min_score = 6
    # Search
    keywords = [
        "backend intern",
        "backend developer intern",
        "backend internship",
        "full stack intern",
        "fullstack intern",
        "software developer intern",
        "devops intern",
        "devops engineer intern",
        "python developer intern",
        "node.js intern",
        "golang intern",
        "backend fresher",
    ]

    location = "India"
    hours_old = 13
    results_per_site = 70
    sites = ["indeed", "linkedin"]

    # Role filter — only these roles allowed
    allowed_roles = [
        "backend",
        "full stack",
        "fullstack",
        "full-stack",
        "devops",
        "devops engineer",
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
        "django",
        "flask",
        "fastapi",
        "express",
        "nestjs",
        "fastify",
        "grpc",
        "postgres",
        "postgresql",
        "mysql",
        "mongodb",
        "docker",
        "kubernetes",
        "redis",
        "aws",
        "gcp",
        "terraform",
        "ansible",
        "jenkins",
        "github actions",
        "gitlab ci",
        "prometheus",
        "grafana",
        "nginx",
        "kafka",
        "linux",
    ]

    # Location filter (remote only)
    allowed_locations = [
        "remote",
        "work from home",
        "wfh",
        "anywhere",
        "distributed",
        "global",
        "home-based",
        "home based",
    ]

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
    turso_url = os.getenv("TURSO_URL")
    turso_token = os.getenv("TURSO_TOKEN")
