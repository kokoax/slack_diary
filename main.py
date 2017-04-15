# coding: utf-8
import os
from slack import SlackBotMain

if __name__ == '__main__':
    # Please execute $ export EVERNOTE_TOKEN="Your evernote token" in terminal.
    slack_token    = os.environ['SLACK_TOKEN']
    evernote_token = os.environ['EVERNOTE_TOKEN']
    sbm = SlackBotMain(slack_token, evernote_token)
