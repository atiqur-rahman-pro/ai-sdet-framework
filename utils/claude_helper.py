from config.config import Config

class ClaudeAIAgent:
    """Helper module integrating Claude AI API for autonomous test triage and prompt analysis."""
    def __init__(self):
        self.api_key = Config.ANTHROPIC_API_KEY

    def analyze_failure(self, test_name: str, stack_trace: str, page_source_snippet: str = "") -> str:
        """Uses Claude AI to perform root-cause analysis on test failure log."""
        prompt = (
            f"You are an expert SDET AI Triage assistant.\n"
            f"Test Case: {test_name}\n"
            f"Stack Trace:\n{stack_trace}\n"
            f"Page Snippet:\n{page_source_snippet[:500]}\n"
            f"Provide a 2-sentence summary of the probable root cause and recommended fix."
        )
        
        if self.api_key:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=self.api_key)
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            except Exception as e:
                return f"Claude AI Call Error: {str(e)}"
        else:
            return (
                f"[Claude AI Offline Triage] Test '{test_name}' failed due to DOM timeout or selector mismatch. "
                f"Suggested Fix: Verify element visibility or update locator in Page Object Model."
            )
