import os
import subprocess
import re
import glob
import argparse
import datetime

# parse command line arguments ------------------------------------------------
parser = argparse.ArgumentParser(description="FastQC, fastq_quality_filter, and STAR pipeline")
parser.add_argument("--dir", type=str,
                    help="Parent folder of fastq files", \
                    default=os.getcwd())
parser.add_argument("--genome", type=str,\
                    help="STAR genome to use",\
                    default="/home/alanrupp/STAR/genome_mm_GRCm38-95")
parser.add_argument("--gtf", type=str,\
                    help="GTF file to use",\
                    default="/home/alanrupp/Documents/Ensembl/Mus_musculus.GRCm38.95.gtf")
parser.add_argument("--nofastqc", \
                    action="store_true", \
                    help="Skip the FASTQC step")
parser.add_argument("--nofilter", \
                    action="store_true", \
                    help="Skip the FASTQ quality filter step")
parser.add_argument("--noalign", \
                    action="store_true", \
                    help="Skip the alignment step")
parser.add_argument('--logfile', \
                    help='Output log file name', \
                    default='log.txt')
args = parser.parse_args()

# mkdir function
def mkdir(directory):
    subprocess.call("mkdir " + directory, shell=True)

# grab software version
def grab_version(program):
    arg = program + ' --version'
    output = subprocess.Popen(arg, stdout=subprocess.PIPE, shell=True).communicate()[0]
    output = output.decode('utf-8')
    return(output)

# FASTQC --------------------------------------------------------------------
def fastqc():
    if args.nofastqc == False:
        mkdir(args.dir + "/FASTQC")
        count = 1
        log = grab_version("fastqc")
        for sample in samples:
            # make directory for FASTQC outputs
            fastqcPath = args.dir + "/FASTQC/" + sample
            mkdir(fastqcPath)
            # pipe files through zcat and FASTQC
            zcat_fastqc = "zcat " + args.dir + '/' + sample + "/*.fastq.gz | " +\
                          "fastqc -t 8 -o " + fastqcPath + " stdin"
            print("\n" + datetime.datetime.now().strftime("%c"))
            print('FASTQC on {}: #{} of {}'.format(sample, count, len(samples)))
            print(zcat_fastqc)
            subprocess.call(zcat_fastqc, shell=True)
            count += 1
            log += zcat_fastqc + '\n'
    else:
        log = 'no FastQC\n'
    return(log + '\n')

# FASTQ quality filter --------------------------------------------------------
def filter(nofilter=False):
    if args.nofilter == False:
        log = 'fastq_quality_filter version 0.0.14\n'
        count = 1
        for sample in samples:
            for read in readset:
                fastq = glob.glob(args.dir + '/' + sample + '/' + '*' + read + \
                                  '*fastq.gz')
                fastq = ' '.join(fastq)
                outPath = args.dir + '/' + sample
                zcat_filter = "zcat " + fastq + " |" +\
                              " fastq_quality_filter -q 20 -z" +\
                              " -o " + outPath + "/" + sample + "_" +\
                              read + "_filtered.fastq.gz"
                print("\n" + datetime.datetime.now().strftime("%c"))
                print('Filtering {}: #{} of {}'.\
                       format(sample, count, len(samples)))
                print(zcat_filter)
                subprocess.call(zcat_filter, shell=True)
            count += 1
            log += zcat_filter + '\n'
    else:
        log = 'no fastq_quality_filter\n'
    return(log + '\n')

# STAR alignment -----------------------------------------------------------
# make directory for output
def STAR():
    if args.noalign == False:
        mkdir(args.dir + '/STAR_outs')
        count = 1
        log = grab_version("STAR")
        for sample in samples:
            # grab reads and parse for paired or unpaired
            mkdir(args.dir + '/STAR_outs/' + sample)
            reads = glob.glob(args.dir + "/" + sample + "/*filtered*")
            if len(reads) == 1:
                read1 = reads[0]
                read2 = ''
            elif len(reads) == 2:
                read1 = [re.findall("R1", read) for read in reads][0]
                read2 = [re.findall("R2", read) for read in reads][0]
            else:
                print('Neither single- nor paired-end reads')
                exit()
            print("\n" + datetime.datetime.now().strftime("%c"))
            print('Aligning {}: #{} of {}'.format(sample, count, len(samples)))
            STAR_align = "~/STAR/bin/Linux_x86_64/STAR" +\
                         " --runThreadN 8" +\
                         " --genomeDir " + args.genome +\
                         " --sjdbGTFfile " + args.gtf +\
                         " --readFilesCommand zcat " +\
                         " --readFilesIn " + read1 + " " + read2 +\
                         " --outFileNamePrefix " + args.dir + "/STAR_outs/" + sample + '/' +\
                         " --outSAMtype BAM SortedByCoordinate" +\
                         " --limitBAMsortRAM 20000000000" +\
                         " --quantMode GeneCounts" +\
                         " --twopassMode Basic"
            print(STAR_align)
            subprocess.call(STAR_align, shell=True)
            log += STAR_align + '\n'
            count += 1
    else:
        log = 'no STAR\n'
    return(log + '\n')

# combine all logs into one
def write_log(*logs, filename=args.logfile):
    out_log = str()
    for log in logs:
        print(log)
        out_log += log
    with open(filename, 'w') as f:
        f.write(out_log)


# - run -----------------------------------------------------------------------
if __name__ == '__main__':
    # get sample
    samples = os.listdir(args.dir)
    mask = [bool(re.match('Sample*', item)) for item in samples]
    samples = [i for (i, match) in zip(samples, mask) if match]

    # detect paired or single end reads:
    files = glob.glob(args.dir + '/*/*.fastq.gz')
    readset = [re.findall("R[1-2]{1}", file)[0] for file in files]
    readset = list(set(readset))

    # fastqc
    fastqc_log = fastqc()

    # filter reads
    filter_log = filter()

    # map to STAR
    star_log = STAR()

    # write a log file
    write_log(fastqc_log, filter_log, star_log)
