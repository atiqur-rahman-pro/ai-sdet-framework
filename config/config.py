import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://sleepapneabd.com")
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    
    # Jira Settings
    JIRA_URL = os.getenv("JIRA_URL", "https://your-domain.atlassian.net")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL", "qa-engineer@example.com")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "mock_jira_token_123")
    JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "QA")
    
    # Claude AI Settings
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
