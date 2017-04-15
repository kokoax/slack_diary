# coding:utf-8
import os
import time
import re
from slackclient import SlackClient

from evnote import EvernoteDiary

class SlackBotMain:
    def __init__(self):
        # Please execute $ export SLACK_TOKEN="Your slack token" in terminal.
        token = os.environ['SLACK_TOKEN']
        self.sc = SlackClient(token)
        self.evdiary = EvernoteDiary()

        if self.sc.rtm_connect():
            print("Connected")
            while True:
                data = self.sc.rtm_read()

                if len(data) > 0:
                    for item in data:
                        self.sc.rtm_send_message("#diary", self.create_message(item))

                time.sleep(0.5)
        else:
            print "Connection Failed, May be invalid token."


    def create_message(self, data):
        if "type" in data.keys():
            if data["type"] == "message":
                if re.search(u"(:diary.*)", data["text"]) is not None:
                    self.evdiary.keepDiary(data["text"][6:])
                    print("Ok I recieved query")
                    return "Ok I recieved query"

