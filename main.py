#! usr/bin/python

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

def get_direct_dl_link(url):
    '''
    Transform a dropbox download link in the form of
        www.dropbox.com/s/{hash}/filename.jpg
    to a direct download link in this format:
        dl.dropboxusercontent.com/s/{hash}/filename.jpg
    '''
    
    return 'http://dl.dropboxusercontent.com' + up.urlparse(url).path

def download_file(url):
    accepted_content_types = ['image/jpeg',
                              'image/png',
                              'image/gif',
                              'image/apng'
                             ]

    dropbox_link = get_direct_dl_link(url)

    r = requests.get(dropbox_link)

    if r.headers['content-type'] in accepted_content_types:
        # Download the link from dropbox (dropbox_link) and rename it to
        # a temporary file. Preserve the file extension.
        tmp_filename = 'tmp' + os.path.splitext(dropbox_link)[1]
	f = open('tmp/' + tmp_filename, 'wb')
        f.write(r.content)
        f.close()

def main():
    config = json.load(open('config.json'))

    r = praw.Reddit(config['user-agent'])
    r.login(config['username'], config['password'])
    submissions = r.get_domain_listing('dropbox.com', sort='new', limit=2)

    #for submission in submissions:
    url = 'https://www.dropbox.com/TESTURL.jpg'
 
    # commented out for testing purposes
    #download_file(url) 

if __name__ == '__main__':
    logging.basicConfig(filename='dropbox-bot.log', level=logging.DEBUG)

    print 'Started Main'
    delete_tmp_files('tmp') # eventually place this at end of main loop
    print 'Finished Main'
