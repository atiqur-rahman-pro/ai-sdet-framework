# Enterprise AI-Augmented QA Automation & SDET Framework

A production-grade, multi-layered QA Engineering & SDET Automation framework demonstrating modern UI, API, AI-Triage, Performance, Technical SEO/A11y, Jira Integration, and CI/CD.

## 🚀 Key Framework Features

1. **E2E Automation (Playwright + Pytest)**: Page Object Model (POM) pattern for robust web test execution.
2. **AI-Powered Triage (Claude AI API)**: Intelligent failure root-cause analysis on stack traces and DOM snippets.
3. **Jira REST API Auto-Ticketing**: Automatic logging of bugs into Jira when tests fail in CI/CD.
4. **Performance Engineering (Locust)**: Code-based distributed load testing in Python.
5. **Technical SEO & A11y Audits**: Automated checks for metadata, headings, and accessibility standards.
6. **Containerization & CI/CD**: Fully dockerized via `Dockerfile` and automated through GitHub Actions workflows.

---

## 📁 Project Architecture

```
ai-sdet-framework/
├── config/
│   └── config.py               # Global environment settings
├── pages/
│   ├── base_page.py            # Base POM class with smart wait helpers
│   ├── home_page.py            # Home page POM
│   └── assessment_page.py      # Health Check Form POM
├── tests/
│   ├── ui/                     # Playwright E2E UI tests
│   ├── api/                    # REST API tests
│   ├── ai/                     # Claude AI autonomous triage & Jira integration tests
│   ├── performance/            # Locust load test scripts
│   └── audit/                  # Technical SEO & A11y tests
├── utils/
│   ├── jira_client.py          # Jira REST API client
│   └── claude_helper.py        # Claude AI API helper
├── docker/
│   └── Dockerfile              # Docker container setup
└── .github/workflows/
    └── main_ci.yml             # GitHub Actions CI/CD workflow
```

---

## 🛠️ How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 2. Execute Pytest Test Suites
- **Run all tests**:
  ```bash
  pytest
  ```
- **Run specific markers**:
  ```bash
  pytest -m ui          # Run UI Playwright tests
  pytest -m api         # Run API tests
  pytest -m ai          # Run AI Triage & Jira integration
  pytest -m audit       # Run Technical SEO tests
  ```

### 3. Run Performance Load Tests (Locust)
```bash
locust -f tests/performance/locustfile.py --headless -u 10 -r 2 -t 30s --host=https://sleepapneabd.com
```

---

## 🐳 Docker Execution
```bash
docker build -t ai-sdet-framework -f docker/Dockerfile .
docker run --rm ai-sdet-framework
```
