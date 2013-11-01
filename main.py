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

def build_comment(imgur_url):
    head = '''Hi! I noticed that you posted an image from dropbox.com. I have
            rehosted your image to imgur because high traffic can break 
            dropbox.com links.\n\n'''

    body = '[Here is the rehosted image](' + imgur_url + ')\n\n'

    tail = '''This action was performed by a bot. If there is an issue or
            problem, please report it below.\n\n'''

    foot = '''[^[DropBox_Bot&nbsp;FAQ]](http://www.reddit.com/r/DropBox_Bot/wiki/faq) 
        [^[Feedback]](http://www.reddit.com/r/DropBox_Bot/submit) 
        [^[Source]](https://github.com/tzoch/dropbox-bot)''' 

    return head + body + tail + foot

def scrape_submissions():
    config = json.load(open('config.json'))
    db = Database(config['database'])

    r = praw.Reddit(config['user-agent'])
    r.login(config['username'], config['password'])
    #submissions = r.get_domain_listing('dropbox.com', sort='new', limit=2)
    # switch the comment out when the bot goes live
    submissions = r.get_subreddit('DropBox_Bot').get_new(limit=10)

    for submission in submissions:
        name = submission.name # makes it easier 
        drop = DropBox(submission.url) 

        if not db.is_processed(submission.name) and drop.is_rehostable:
            drop.download_file()
            imgur_url = drop.rehost_image()

            if imgur_url:
                comment = build_comment(imgur_url)
                submission.add_comment(comment)
                db.mark_as_processed(name)
                logging.info('Success! [' + name + '] rehosted')
            else:
                logging.error('Failure! [' + name + '] error while uploading')
        else:
            db.mark_as_processed(name)
            logging.info('Skipped! [' + name + '] is not rehostable')

def main():
    pass

if __name__ == '__main__':
    fmt = '[%(asctime)-15s] (%(module)-15s) %(levelname)-8s : %(message)s'
    logging.basicConfig(filename='dropbox-bot.log', 
                        format=fmt,
                        datefmt='%d-%b %H:%M:%S',
                        level=logging.INFO)

    print 'Started Main'
    scrape_submissions()
    print 'Finished Main'
