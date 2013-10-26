#! /usr/bin/python

'''Some utility and debugging functions for the Dropbox Bot'''

import hashlib
import logging
import os
import time

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

def delete_tmp_files(directory):

    files_to_delete = os.listdir(directory)
    i = 0
    t = time.strftime('%H:%M:%S')

    if files_to_delete:
        for tmp_file in files_to_delete:
            os.remove(directory + '/' + tmp_file)
            i += 1

        logging.info('[%s] Temporary Files Clear! %s files deleted', t, i)
        return
    else:
        logging.info('[%s] Temporary Files Clear! No Files to delete', t) 
        return

if __name__ == '__main__':
    print generate_thing_ids(5)
