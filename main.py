#! usr/bin/python

import time
import json
import logging
import sqlite3

import requests
import praw

def main():
    config = json.load(open('config.json'))

    r = praw.Reddit(config['user-agent'])
    r.login(config['username'], config['password'])

if __name__ == '__main__':
    main()
    print 'Main Executed'
