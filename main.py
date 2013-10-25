#! usr/bin/python

import time
import json
import logging

import urlparse as up

import requests
import praw
import pyimgur

from database import Database

supported_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

def get_direct_dl_link(url):
    '''
    Transform a dropbox download link in the form of
        www.dropbox.com/s/{hash}/filename.jpg
    to a direct download link in this format:
        dl.dropboxusercontent.com/s/{hash}/filename.jpg
    '''
    
    return 'http://dl.dropboxusercontent.com' + up.urlparse(url).path


def main():
    config = json.load(open('config.json'))

    r = praw.Reddit(config['user-agent'])
    r.login(config['username'], config['password'])
    submissions = r.get_domain_listing('dropbox.com', sort='new', limit=2)
    
    for submission in submissions:
        print vars(submission)

if __name__ == '__main__':
    print 'Started Main'
    main()
    print 'Finished Main'
