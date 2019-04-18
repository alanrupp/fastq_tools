"""
Create a CSV file of GO terms and genes from GAF file
"""

import re
import subprocess

def open_gz(file):
    output = subprocess.check_output('zcat ' + file, shell=True)
    output = output.decode('UTF-8')
    output = output.split('\n')
    print('Reading file: ' + str(len(output)) + ' lines')
    return(output)

def gaf_to_dict(gaf):
    results = dict()
    for line in gaf:
        if line.startswith('!'): continue
        else:
            gene = line.split()[2]
            go_term = line.split()[3]
            if go_term.startswith('GO'):
                results.setdefault(go_term, []).append(gene)
    print('Processing GO terms: ' + str(len(results)) + ' terms')
    return(results)

def write_csv(d, csv_file):
    print('Writing CSV file: ' + csv_file)
    with open(csv_file, 'w') as f:
        f.write('GO,gene\n')
        for key in list(d.keys()):
            for value in d[key]:
                f.write(key + ',' + value + '\n')

def gzip(file):
    print('Gzipping ' + file)
    subprocess.call('gzip ' + file, shell=True)

if __name__ == '__main__':
    # process command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input file (gzip GAF format)')
    parser.add_argument('-o', help='output file (*.csv)')
    parser.add_argument('--gzip', help='gzip output', action='store_true')
    args = parser.parse_args()

    # read in data, generate dictionary, and write
    gaf = open_gz(args.i)
    gaf_dict = gaf_to_dict(gaf)
    write_csv(gaf_dict, args.o)
    if args.gzip:
        gzip(args.o)
    print('Done')
