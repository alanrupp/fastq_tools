#!/usr/bin/python

'''
Mapping 10X data with cellranger
'''

import subprocess
import re

def unzip(file):
    out = f"gunzip {file}"
    
    return

def make_premrna(gtf):
    if re.search("gz$", gtf):
        unzip(gtf)
    out_file = f"{gtf}_premrna.gtf"
    out = "awk 'BEGIN{FS="
    out += '"\\t"; OFS="\\t"} $3 == "transcript"{ $3="exon"; print}'
    out += f" {gtf} > {out_file}"
    print(out)
    return out_file

def mkref(genome, fasta, gtf, threads=8):
    out = f"cellranger mkref genome={genome} fasta={fasta} genes={gtf} "
    out += f"--nthreads={threads}"
    #print(out)
    #subprocess.call(out, shell=True)

if __name__ == '__main__':
    ensembl_dir = '/home/alanrupp/Documents/Ensembl'
    import argparse
    parser = argparse.ArgumentParser(description='Map 10X data with cellranger')
    parser.add_argument('--genome', default="genome")
    parser.add_argument('--fasta', default=f"{ensembl_dir}/Mus_musculus.GRCm38.dna.primary_assembly.fa.gz")
    parser.add_argument('--gtf', default=f"{ensembl_dir}/Mus_musculus.GRCm38.98.gtf.gz")
    parser.add_argument('--threads', default=8)
    parser.add_argument('--nuclei', action='store_true')
    args = parser.parse_args()

    if args.nuclei:
        args.gtf = make_premrna(args.gtf)

    # mkref
    mkref(args.genome, args.fasta, args.gtf, args.threads)
