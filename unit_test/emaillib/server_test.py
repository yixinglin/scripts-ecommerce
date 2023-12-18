# python server_test -m dev
# Test RestAPI for Bulk Service
import os
import sys

from pylib.ioutils import base64encode_urlsafe

sys.path.append(".")
sys.path.append("./emaillib")
import unittest
from emaillib.glo import OS_TYPE, EmailApplication
from emaillib.rest.SendLatterRestApi import SendLatterRestApi
from emaillib import load_yaml

import random


class TestEmailRestAPI:

    def __init__(self):
        debug = True
        conf_path = os.path.join("emaillib", "config-docker.yaml")
        conf = load_yaml(conf_path)
        # os.path.join(conf['log'][OS_TYPE]['path'])
        self.app = EmailApplication(conf_path, debug=debug)
        self.api = SendLatterRestApi(conf)
        nums = random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 9)
        self.username = "".join(nums)
        self.testcase = unittest.TestCase()
        pass

    def test_api_new_email(self):
        # Test New Email
        new_email = f"{self.username}@example.com"
        print(":test_api_new_email ", new_email)
        # Get email
        res = self.api.registered_email(new_email).content
        self.testcase.assertEqual(res['total'], 0)
        self.testcase.assertEqual(len(res['data']), 0)

        # Mark as Sent
        res = self.api.update_to_sent(new_email).content
        self.testcase.assertEqual(res, 'sent')
        # Cancel Subscription
        res = self.api.update_to_unsub(email_addr=new_email).content
        # Get registered email
        res = self.api.registered_email(new_email).content
        self.testcase.assertEqual(res['data'][0]['addr'], new_email)
        self.testcase.assertEqual(res['data'][0]['unsubscribed'], True)
        self.testcase.assertEqual(res['data'][0]['send_permitted'], False)

        #  Subscription
        res = self.api.update_to_sub(new_email).content
        # Get registered email
        res = self.api.registered_email(new_email).content
        self.testcase.assertEqual(res['data'][0]['addr'], new_email)
        self.testcase.assertEqual(res['data'][0]['unsubscribed'], False)
        self.testcase.assertEqual(res['data'][0]['send_permitted'], False)
        pass

    def test_api_old_email(self):
        # Get email
        target_email = "username11@example.com"
        print(":target_email ", target_email)
        res = self.api.registered_email(target_email).content
        encoded = base64encode_urlsafe(target_email)
        self.testcase.assertEqual(res['data'][0]['send_permitted'], True)
        self.testcase.assertEqual(res['data'][0]['encoded'], encoded)

if __name__ == '__main__':
    a = TestEmailRestAPI()
    a.test_api_new_email()
    a.test_api_old_email()
    print("TestEmailRestAPI: Test Finish")
    pass
