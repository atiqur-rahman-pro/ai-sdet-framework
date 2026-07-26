from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def load_homepage(self):
        self.client.get("/")

    @task(1)
    def load_assessment_page(self):
        self.client.get("/sleep-apnea-assessment")

    @task(1)
    def load_about_page(self):
        self.client.get("/about-us")
