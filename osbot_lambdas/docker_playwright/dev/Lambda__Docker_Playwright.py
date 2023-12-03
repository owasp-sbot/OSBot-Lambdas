from osbot_lambdas.docker_playwright.dev.Build_Deploy__Docker_Playwright import Build_Deploy__Docker_Playwright


class Lambda__Docker_Playwright:

    def __init__(self):
        self.build_deploy = Build_Deploy__Docker_Playwright()

    def build_docker_image(self):
        return self.build_deploy.build_docker_image()

    def publish_docker_image(self):
        return self.build_deploy.create_image_ecr.push_image()

    def create_lambda_function(self, delete_existing=True, wait_for_active=True):
        return self.build_deploy.create_lambda(delete_existing=delete_existing, wait_for_active=wait_for_active)

    def update_lambda_function(self, wait_for_update=True):
        result = self.build_deploy.update_lambda_function()
        if wait_for_update is False:
            return result.get('LastUpdateStatus')
        return self.build_deploy.lambda_function().wait_for_function_update_to_complete(wait_time=1)        # this takes a while so make the interval to be 1 sec before checks


    def rebuild_and_publish(self):
        build_result   = self.build_docker_image()
        publish_result = self.publish_docker_image()
        update_result  = self.update_lambda_function()
        return dict(build_result=build_result, publish_result=publish_result, update_result=update_result)
