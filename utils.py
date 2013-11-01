#! /usr/bin/python

'''Some utility and debugging functions for the Dropbox Bot'''

import logging
import os

def delete_tmp_files(directory='tmp'):
    '''Delete temporary files and log result'''

    files_to_delete = os.listdir(directory)
    i = 0

    if files_to_delete:
        for tmp_file in files_to_delete:
            os.remove(directory + '/' + tmp_file)
            i += 1

        logging.info('Temporary files cleared! [%s] deletd')
        return
    else:
        logging.info('Temporary files cleared! No files to delete') 
        return

if __name__ == '__main__':
    delete_tmp_files()
