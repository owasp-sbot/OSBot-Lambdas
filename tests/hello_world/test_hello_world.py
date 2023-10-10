from unittest import TestCase

from osbot_lambdas.hello_world.handler import run


class test_hello_world(TestCase):

    def setUp(self) -> None:
        self.handler_run = run

    def test_execute_directly(self):
        assert self.handler_run({}) == 'hello world!'