#!/usr/bin/python

'''
Mapping 10X data with cellranger. First create a reference with mkref and then
map and count with count.
'''

import subprocess
import re
import os

def unzip(file):
    out_file = re.findall(file, "(.+)(?=\.gz)")[0]
    out = f"gunzip {file}"
    print(out_file)
    #subprocess.call(out, shell=True)
    return out_file

def make_premrna(gtf):
    out_file = f"{gtf}_premrna.gtf"
    out = "awk 'BEGIN{FS="
    out += '"\\t"; OFS="\\t"} $3 == "transcript"{ $3="exon"; print}'
    out += f" {gtf} > {out_file}"
    print(out)
    return out_file

def mkref(genome, fasta, gtf, threads=8):
    out = f"cellranger mkref genome={genome} fasta={fasta} genes={gtf} "
    out += f"--nthreads={threads}"
    print(out)
    #subprocess.call(out, shell=True)

# add a link function to circumvent problems with spaces in path names
def link(fastq_dir):
    mkdir = "mkdir ~/Desktop/soft_link"
    print(mkdir)
    #subprocess.call(out, shell=True)
    files = os.listdir(fastq_dir)
    for file in files:
        out = f"ln -s {file} ~/Desktop/soft_link"
        print(out)

def count(id, fastq, sample, transcriptome, no_secondary=True):
    out = "cellranger count "
    out += f"--id={id} "
    out += f"--fastqs={fastq} "
    out += f"--sample={sample} "
    out += f"--transcriptome={transcriptome} "
    out += "--expect-cells=10000 "
    if no_secondary:
        out += "--nosecondary"
    print(out)
    #subprocess.call(out, shell=True)

def remove(file, recursive=True):
    if recursive:
        out = f"rm -r {file}"
    else:
        out = f"rm {file}"
    print(out)
    #subprocess.call(out, shell=True)

if __name__ == '__main__':
    ensembl_dir = '/home/alanrupp/Documents/Ensembl'
    import argparse
    parser = argparse.ArgumentParser(description='Map 10X data with cellranger')
    parser.add_argument('--genome', default="genome")
    parser.add_argument('--fasta', default=f"{ensembl_dir}/Mus_musculus.GRCm38.dna.primary_assembly.fa")
    parser.add_argument('--gtf', default=f"{ensembl_dir}/Mus_musculus.GRCm38.98.gtf")
    parser.add_argument('--threads', default=8)
    parser.add_argument('--nuclei', action='store_true')
    parser.add_argument('--link', action='store_true')
    parser.add_argument('--id')
    parser.add_argument('--fastq')
    parser.add_argument('--sample')
    parser.add_argument('--transcriptome', default='genome')
    args = parser.parse_args()

    # unzip if files are gzipped
    if re.search("gz$", args.fasta):
        args.fasta = unzip(args.fasta)
    if re.search("gz$", args.gtf):
        args.gtf = unzip(args.gtf)

    # make premrna references if nuceli flag
    if args.nuclei:
        args.gtf = make_premrna(args.gtf)

    # mkref
    mkref(args.genome, args.fasta, args.gtf, args.threads)

    # count
    if args.link:
        args.fastq = link(args.fastq)
    count(args.id, args.fastq, args.sample, args.transcriptome)

    # remove genome
    remove('genome')
    remove('~/Desktop/soft_link')
