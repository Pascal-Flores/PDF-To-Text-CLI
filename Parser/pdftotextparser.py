#!/usr/bin/python

import os
import subprocess
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Convert pdftotext output to a custom txt file')
parser.add_argument('file', help='a pdf file', type=str)
parser.add_argument('-o', '--output', help='output file', type=str)

args = parser.parse_args()

# generates the txt version of the input file
subprocess.run(["pdftotext", "-raw", args.file, args.file+'.txt'])

pdftotxt = open(args.file+'.txt')
# creates the output file
outfile = None
if args.output:
    outfile = open(args.output, 'w')
else:
    outfile = open(Path(args.file).stem, 'w')

#write the name of the file with spaced replaced by underscores
outfile.write(os.path.basename(args.file).replace(' ', '_'))

# deletes the txt version of the input file
os.remove(args.file+'.txt')



