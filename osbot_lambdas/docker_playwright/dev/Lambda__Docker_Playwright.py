from osbot_lambdas.docker_playwright.dev.Build_Deploy__Docker_Playwright import Build_Deploy__Docker_Playwright


class Lambda__Docker_Playwright:

    def __init__(self):
        self.build_deploy = Build_Deploy__Docker_Playwright()

    def build_docker_image(self):
        return self.build_deploy.build_docker_image()
