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
from utils import delete_tmp_files
from dropbox import DropBox

def main():
    config = json.load(open('config.json'))

    r = praw.Reddit(config['user-agent'])
    r.login(config['username'], config['password'])
    submissions = r.get_domain_listing('dropbox.com', sort='new', limit=2)

    for submission in submissions:
        print submission.name
 
if __name__ == '__main__':
    logging.basicConfig(filename='dropbox-bot.log', level=logging.DEBUG)

    print 'Started Main'
    main()
    print 'Finished Main'

