import requests
import json
from config.config import Config

class JiraClient:
    """Client for logging bug tickets automatically into Jira REST API on test failure."""
    def __init__(self):
        self.jira_url = Config.JIRA_URL
        self.email = Config.JIRA_EMAIL
        self.api_token = Config.JIRA_API_TOKEN
        self.project_key = Config.JIRA_PROJECT_KEY

    def create_issue(self, summary: str, description: str, issue_type: str = "Bug"):
        url = f"{self.jira_url}/rest/api/3/issue"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        print(f"[Jira Integration] Mock/Real Logging issue: {summary}")
        # In live env with real tokens, send request:
        # response = requests.post(url, json=payload, headers=headers, auth=(self.email, self.api_token))
        # return response.json()
        return {"key": f"{self.project_key}-101", "status": "Created (Mock)"}
