from unittest import TestCase

from dotenv                 import load_dotenv
from osbot_aws.AWS_Config   import AWS_Config
from osbot_aws.apis.S3      import S3
from osbot_aws.apis.STS     import STS

OSBOT_AWS_ACCOUNT_ID     = '470426667096'
OSBOT_AWS_DEFAULT_REGION = 'eu-west-2'
OSBOT_AWS_DEPLOY_USER    = 'GitHub-Deploy-User'

class test_check_AWS_Config(TestCase):

    def setUp(self):
        load_dotenv()
        self.aws_config = AWS_Config()
        self.sts        = STS()

    def test_check_aws_credentials(self):
        assert self.aws_config.aws_session_account_id () == OSBOT_AWS_ACCOUNT_ID
        assert self.aws_config.aws_session_region_name() == OSBOT_AWS_DEFAULT_REGION

        self.sts.check_current_session_credentials()
        assert self.sts.current_account_id()             == OSBOT_AWS_ACCOUNT_ID
        assert self.sts.current_region_name()            == OSBOT_AWS_DEFAULT_REGION

        assert self.sts.caller_identity_arn()            == f'arn:aws:iam::{OSBOT_AWS_ACCOUNT_ID}:user/{OSBOT_AWS_DEPLOY_USER}'

    def test_osbot_setup(self):
        account_id = self.aws_config.aws_session_account_id ()
        assert f'{account_id}-osbot-lambdas' in S3().buckets()
