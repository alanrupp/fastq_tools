#!/usr/bin/python

'''
Functions to get data for GEO submissions
'''

import glob
import subprocess
import re

def md5sum(file):
    # get md5sum from a given file
    print(f"md5sum {file}")
    p = subprocess.Popen(['md5sum', file], stdout=subprocess.PIPE)
    p = p.communicate()[0].decode('utf-8')
    p = re.findall("^\S+", p)[0]
    return p

def stats(file):
    # get BAM file stats from samtools stats
    print(f"samtools stats {file}")
    p = subprocess.Popen(['samtools', 'stats', file], stdout=subprocess.PIPE)
    p = p.communicate()[0].decode('utf-8')
    return p

def inserts(file):
    # get insert size average and standard deviation from samtools stats output
    p = stats(file)
    p = p.split('\n')
    for line in p:
        if re.search('insert size average', line):
            average = re.findall("\S+$", line)[0]
        if re.search('insert size standard deviation', line):
            stdev = re.findall("\S+$", line)[0]
    return average, stdev
