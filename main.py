#! /usr/bin/python

import json
import logging
import os
import time

import urlparse as up

import praw
import requests

from database import Database
from utils import delete_tmp_files
from dropbox import DropBox

def build_comment(imgur_url):
    head = '''Hi! I noticed that you posted an image from dropbox.com. I have rehosted your image to imgur because high traffic can break dropbox.com links.\n\n'''

    body = '[Here is the rehosted image](' + imgur_url + ')\n\n'

    tail = '''This action was performed by a bot. If there is an issue or
            problem, please report it below.\n\n'''

    foot = '''[^[Bot&nbsp;FAQ]](http://www.reddit.com/r/DropBox_Bot/wiki/index)
        [^[Report&nbsp;Problem]](http://www.reddit.com/message/compose/?to=DropBox_Bot&subject=Problem%20to%20Report)
        [^[Feedback]](http://www.reddit.com/r/DropBox_Bot/submit) 
        [^[Source]](https://github.com/tzoch/dropbox-bot)''' 

    return head + body + tail + foot

def scrape_domain_submissions(domain, config, r):
    '''
    This is the main work horse function of the dropbox bot. The bot gets the
    latest submissions to the dropbox.com domain and checks for two conditions.
        1. If it has already processed the submission, the bot skips it
        2. If it is able to be rehosted, we processes it
            - currently, the bot only supports the rehosting of images, but
              if there is a demand for other formats, and if there are 
              convinient hosts to use, they will be implemented

    Currently, there is some basic logging to report the status of the bot.
    However, proper error handling should be added to make sure bad requests
    or 404'd dropbox pages are skipped and do not crash the bot.
    '''

    db = Database(config['database'])

    if config['test-mode']:
        submissions = r.get_subreddit('DropBox_Bot').get_new(limit=10)
    else:
        submissions = r.get_domain_listing(domain, sort='new', limit=100)

    for submission in submissions:
        name = submission.name # the thing_id - easier to reassign here 
        drop = DropBox(submission.url, name)

        # first, make sure the submission hasn't been processed already
        if db.is_processed(name):
            logging.info('Skipped! [' + name + '] has already been processed')
            continue

        # skip deleted comments and blaklisted users
        if not submission.author:
            logging.info('Skipped! [' + name + '] Submission has been deleted')
            db.mark_as_processed(name)
            continue
        elif submission.author.name.lower() in config['user_blacklist']:
            logging.info('Skipped! [' + name + '] is by a blacklisted author')
            db.mark_as_processed(name)
            continue

        # skip blacklisted subreddits
        if submission.subreddit.display_name.lower() in config['blacklist']:
            logging.info('Skipped! [' + name + '] in a blacklisted subreddit')
            db.mark_as_processed(name)
            continue

        if drop.is_rehostable:
            drop.download_file()
            img = drop.rehost_image()

            # This will return false from the dropbox.py file
            # if there is an HTTP Exception uploading the file
            if imgur_url:
                comment = build_comment(img.link)
                # These try/excepts are to help get around the
                # commenting limit reddit has for new accounts
                try:
                    submission.add_comment(comment)
                    db.mark_as_processed(name)
                    db.log_image(img.id, img.deletehash)
                except requests.exceptions.HTTPError:
                    logging.error('ERROR! [' + name + '] HTTP Error')
                    logging.info(name + ' in subreddit ' + submission.subreddit.display_name) 
                    print 'Failed to rehost [' + name + '] due to HTTPError'
                except praw.errors.RateLimitExceeded:
                    logging.error('ERROR! [' + name + '] RateLimtitExceeded')
                    logging.info('Trying to sleep off the RateLimit')
                    time.sleep(1200)
                    logging.info('AWAKE! Trying to comment again...')
                    try:
                        submission.add_coment(comment)
                        db.mark_as_processed(name)
                    except praw.errors.RateLimitExceeded:
                        logging.error('Skipped! [' + name + '] Rate Limited')
                        continue
                logging.info('Success! [' + name + '] rehosted')
            # This probably hapens due to an imgur API error
            # ex. the file is too large to be uploaded, so we
            # should skip and mark as processed
            else:
                logging.error('Failure! [' + name + '] error while uploading')
                db.mark_as_processed(name)
        else:
            db.mark_as_processed(name)
            logging.info('Skipped! [' + name + '] is not rehostable')

def main():
    fmt = '[%(asctime)-15s] (%(module)-15s) %(levelname)-8s : %(message)s'
    logging.basicConfig(filename='dropbox-bot.log', 
                        format=fmt,
                        datefmt='%d-%b %H:%M:%S',
                        level=logging.INFO)

    logging.info('Bot Started')

    print '''DropBox Bot started...\n\tTo monitor the bots status check the log
             "dropbox-bot.log"\n\tTo stop the bot, use KeyboardInterrupt'''

    while True:
        print 'Loading Config'
        config = json.load(open('config.json'))

        print 'Logging In'
        r = praw.Reddit(config['user-agent'])
        r.login(config['username'], config['password'])

        try:
            print 'Scraping Submissions'
            scrape_domain_submissions('dropbox.com',
                                      config, r)
            scrape_domain_submissions('dl.dropboxusercontent.com', 
                                      config, r)
            print 'Finished Scraping'
        except KeyboardInterrupt:
            import sys
            sys.exit(0)

        delete_tmp_files()
        print 'Finished Processing\nSleeping for 20 minutes'
        logging.info('Sleeping! No new submissions to process')
        time.sleep(1200)

if __name__ == '__main__':
    print '[INITIALIZED]'
    main()
