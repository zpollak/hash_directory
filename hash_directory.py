#!/usr/bin/env python

import csv
import datetime
import hashlib as hl
import logging
import os
import sys

def clean_datetime():
    
    return str(datetime.datetime.now().replace(second=0, microsecond=0)).replace(':', '').replace(' ', '_')[:-2]

def write_csv(tups_list, filename): 
    with open(filename,'wb') as f:
        csv_out = csv.writer(f)
        csv_out.writerow(['File_Name','MD5_Hash'])
        for row in tups_list:
            csv_out.writerow(row)
    
def file_hasher(fn):
    with open(fn, 'rb') as f:
        dt = f.read()
        fhash = hl.md5(dt).hexdigest()
    
    return fhash

def hash_directory(directory=None):
    if directory == None: 
        print('Need a directory.')
        sys.exit()
    hashed_files = []
    for root, dirs, files in os.walk(directory):
        for fn in files:
            try:
                fn_hash = file_hasher(os.path.join(root, fn))
                hashed_files.append(tuple([fn, fn_hash]))
                print(fn + ' hash: ' + str(fn_hash))
            except Exception as e:
                print(fn + ': ' + str(e))
                logging.error(e)
    
    return hashed_files

def dir_prompt():
    print('Enter the directory with files to hash.')
    print('If you wish to hash the directory containing this script, just press <Enter>.')
    print('Please note this script will hash all files in the directory and all subdirectories.')
    directory = raw_input()
    if directory == '':
        directory = os.getcwd()
    
    return directory

def main():
    fn_output = 'hashed_files_' + clean_datetime() + '.csv'
    fn_log = 'hash_log_' + clean_datetime() + '.log'
    logging.basicConfig(filename=fn_log, filemode='w', level=logging.DEBUG)
    hashes = hash_directory(dir_prompt())
    write_csv(hashes, fn_output)

if  __name__ == '__main__':
    main()
