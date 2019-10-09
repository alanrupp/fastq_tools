#!/usr/bin/python
import subprocess
import re

def make_expression(expt):


def move(file):
    cmd = f"mv {file} /opt/DEPICT/data/tissue_expression"
    subprocess.call(cmd, shell=True)
    print(f"moving {file} to DEPICT folder\n")

def delete(file):
    cmd = f"rm /opt/DEPICT/data/tissue_expression/{file}"
    subprocess.call(cmd, shell=True)
    print(f"deleting {file} from DEPICT folder\n")

def cfg(folder):
    with open('example.cfg', 'r') as f:
        file = f.read()




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    args.add_argument('name', help='input file')

    move(args.name)
    delete(args.i)
