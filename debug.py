#! /usr/bin/python

'''Some utility and debugging functions for the Dropbox Bot'''

import time
import hashlib

def generate_thing_ids(n):
    '''
    Generate random, valid reddit thing_ids

    @param n: number of thing_ids to generate
    @param output: either string or list
    @return: a list of thing_ids
    '''

    def thing_id(seed):
        random = hashlib.md5(str(time.time() + seed))
        return 't3_' + random.hexdigest()[:7]
        

    output = []

    for i in range(n):
        output.append(thing_id(i))

    return output

if __name__ == '__main__':
    print generate_thing_ids(5)
