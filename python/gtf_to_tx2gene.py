## Make a tx2gene CSV file from GTF
import numpy as np
import pandas as pd
import argparse
import re
import os

# function to grab info associated with user input fields
def grab_info(field):
    info = re.findall(field + ' \"(.*?)\"', line)
    if len(info) == 0:
        info = ""
    else:
        info = info[0]
    return(info)

# set up argsparse
parser = argparse.ArgumentParser(description='Convert a GTF file to CSV')
parser.add_argument('--gtf', help='input GTF file', type=str)
parser.add_argument('--fields', help='fields to pull', \
                    default=['transcript_id', 'transcript_name', 'gene_id',\
                             'gene_name', 'gene_biotype'],
                    nargs='*')
parser.add_argument('--csv', help='output CSV file', type=str)
parser.add_argument('--sample', help='first n lines to sample for keys (default=1000)', \
                    type=int, default=1000)
parser.add_argument('--head', help='lines to read for generating list of fields',\
                    default=1000)
args = parser.parse_args()

# make sure GTF file exists
if os.path.isfile(args.gtf):
    gtf = args.gtf
else:
    print('\nGTF file does not exist')
    exit()

# ensure transcript_id is in fields argument
if 'transcript_id' not in args.fields:
    print('Error: transcript_id is required field')
    exit()
else:
    transcript_id = np.where(np.array(args.fields) == 'transcript_id')[0][0]

# check to see

# check to see if fields are in GTF file
with open(args.gtf, 'r') as f:
    count = 0
    while count < args.head:
        all_fields = list()
        for line in f:
            count += 1
            if line.startswith('#'): continue # skip header lines
            line = line.split(sep='\t')[8]
            fields = re.findall('([\\S]+) {1}\"[\\S]+\"', line)
            all_fields = list(set(all_fields).union(fields))
for field in args.fields:
    if field not in all_fields:
        print('Warning: ' + field + ' not in first ' + str(lines_read) + ' lines of the GTF')

# generate dictionary from GTF file
tx2gene = dict()
with open(gtf, 'r') as f:
    for line in f:
        if line.startswith('#'): continue # skip header lines
        line = line.split(sep='\t')[8]
        field_stash = list()
        for field in args.fields:
            hit = grab_info(field)
            field_stash.append(hit)
        # if the transcript_id is new, add it to the dictionary with its info
        if field_stash[transcript_id] not in tx2gene.keys():
            tx2gene[field_stash[transcript_id]] = np.array(field_stash)[np.arange(len(field_stash)) != transcript_id]
        else: continue

# turn into data frame for easy output
tx2gene = pd.DataFrame.from_dict(tx2gene, orient='index')
tx2gene.reset_index(level=0, inplace=True)
rename_col = {'index': 'transcript_id'}
if len(args.fields) > 1:
    count = 0
    for field in args.fields:
        if field == 'transcript_id': continue
        else:
            rename_col[count] = field
            count += 1
tx2gene.rename(columns=rename_col, inplace=True)

# write to CSV file
output = args.csv
tx2gene.to_csv(output, index=False)
