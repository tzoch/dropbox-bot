#! usr/bin/python

import json
import logging
import os

import urlparse as up

import requests
import praw
import pyimgur

from database import Database
from utils import delete_tmp_files

class DropBox(object):

    def __init__(self, url, title=None):

        self.working_url = self.get_direct_link(url)
        self.title = title
        self.config = json.load(open('config.json'))

        self.accepted_content_types = ['image/jpeg',
                                       'image/png',
                                       'image/gif',
                                       'image/apng'
                                      ]

        self.max_file_size = 5242880 # 5 mb (limit for imgur non-premium)

    def get_direct_link(self, url):
        '''
        Transform a dropbox download link in the form of
            www.dropbox.com/s/{hash}/filename.jpg
        to a direct download link in this format:
            dl.dropboxusercontent.com/s/{hash}/filename.jpg
        '''
        return 'http://dl.dropboxusercontent.com' + up.urlparse(url).path

    @property
    def is_rehostable(self):
        '''
        Determine if the working url can be rehosted to imgur.
        Checks if the file is under the acceptable filesize and of a valid
        content-type.

        @param url: str of dropboxurl (from self.working_url)
        @return bool
        '''

        r = requests.head(self.working_url)
        
        if r.headers['content-type'] in self.accepted_content_types:
            # Type cast content-length for accurate comparison
            if int(r.headers['content-length']) < self.max_file_size:
                return True

        return False

    def download_file(self):

        r = requests.get(self.working_url)

        if self.is_rehostable:
            # Download the link from dropbox (dropbox_link) and rename it to
            # a temporary file. Preserve the file extension with
            # os.path.splittext
            self.tmp_filename = 'tmp' + os.path.splitext(self.working_url)[1]
            f = open('tmp/' + self.tmp_filename, 'wb')
            f.write(r.content)
            f.close()

    def rehost_image(self):
        '''
        Upload the image in the tmp directory to imgur. Function returns
        the imgur url to the rehosted image as a string.

                
        '''
        im = pyimgur.Imgur(self.config['imgur_api']['client_id'])
        path = 'tmp/' + self.tmp_filename
        uploaded_image = im.upload_image(path, self.title) 
        return uploaded_image.link

if __name__ == '__main__':
    logging.basicConfig(filename='dropbox-bot.log', level=logging.DEBUG)

    print 'Started Main'
    url = 'https://www.dropbox.com/s/i7st517rya0isv6/roadside%20sign.jpg'
    dp = DropBox(url)
    dp.download_file()
    print dp.rehost_image()
    print 'Finished Main'

