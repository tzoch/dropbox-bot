#! /usr/bin/python

import json
import time
import logging

import praw

from database import Database

class RedditBot(object):

    def __init__(self):
        self.monitor_domains = ['dropbox.com', 'dl.dropboxusercontent.com'] 
        self.config = json.load(open('config.json'))

        self.db = Database(self.config['database'])

        self.r = praw.Reddit(self.config['user-agent']) 
        self.r.login(self.config['username'], self.config['password'])

    def process_submissions(self, domain):
        submissions = self.r.get_domain_listing(domain, sort='new', limit=100)
        for submission in submissions:
            print submission.url

if __name__ == '__main__':
    rb = RedditBot()
    rb.process_submissions('dropbox.com')
