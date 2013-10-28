#! /usr/bin/python

import json
import logging
import os
import time

import urlparse as up

import requests
import praw
import pyimgur

from database import Database
from debug import delete_tmp_files
from dropbox import DropBox

def main():
    config = json.load(open('config.json'))

    r = praw.Reddit(config['user-agent'])
    r.login(config['username'], config['password'])
    submissions = r.get_domain_listing('dropbox.com', sort='new', limit=2)

    #for submission in submissions:
    url = 'https://www.dropbox.com/TESTURL.jpg'
 
if __name__ == '__main__':
    logging.basicConfig(filename='dropbox-bot.log', level=logging.DEBUG)

    print 'Started Main'
    print 'Finished Main'

