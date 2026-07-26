import pytest
from utils.claude_helper import ClaudeAIAgent
from utils.jira_client import JiraClient

@pytest.mark.ai
def test_claude_ai_triage_simulation():
    """Simulate test failure and verify Claude AI triage analysis & Jira ticket creation."""
    ai_agent = ClaudeAIAgent()
    jira = JiraClient()
    
    mock_test_name = "test_checkout_payment_flow"
    mock_stack_trace = "ElementNotFoundError: Selector '#pay-now-btn' not visible within 30000ms"
    mock_html_snippet = "<button class='btn-primary' id='submit-payment-btn'>Pay Now</button>"
    
    # 1. Claude AI Analysis
    triage_result = ai_agent.analyze_failure(mock_test_name, mock_stack_trace, mock_html_snippet)
    print("\n🤖 Claude AI Root Cause Summary:\n", triage_result)
    assert len(triage_result) > 0
    
    # 2. Auto Jira Bug Creation
    jira_response = jira.create_issue(
        summary=f"Automated Failure: {mock_test_name}",
        description=f"AI Triage Analysis:\n{triage_result}\n\nStack Trace:\n{mock_stack_trace}"
    )
    assert jira_response["key"].startswith("QA-")
