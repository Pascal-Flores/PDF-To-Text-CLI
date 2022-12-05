import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Convert pdftotext output to a custom txt file')
parser.add_argument('file', help='a pdf file')
parser.add_argument('-o', '--output', help='output file')

args = parser.parse_args()

outfile = None
if args.output:
    outfile = open(args.output, 'w')
else:
    outfile = open(Path(args.file).stem, 'w')

#write the name of the file with spaced replaced by underscores
outfile.write(os.path.basename(args.file).replace(' ', '_'))
