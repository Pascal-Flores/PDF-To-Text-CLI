#!/usr/bin/python

import os
import subprocess
import argparse
from pathlib import Path

import abstract

# for each file in the directory located in ../CORPUS_TRAIN
# run pdftotext on the file and save the output to a text file in the directory ../CORPUS_TRAIN_TXT
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the directory containing the pdf files")
    args = parser.parse_args()
    path = args.path

    if not os.path.exists(path + "_TXT"):
        os.makedirs(path + "_TXT")
    elif os.listdir(path + "_TXT"):
        for file in os.listdir(path + "_TXT"):
            os.remove(path + "_TXT/" + file)

    for file in os.listdir(path):
        if file.endswith(".pdf"):
            print("Processing file: " + file)
            pdf_file = Path(path + "/" + file)
            txt_file = Path(path + "_TXT/" + file + ".txt")
            if not txt_file.is_file():
                subprocess.call(["pdftotext", "-raw", pdf_file, txt_file])
                print ("Created temporary text file: " + str(txt_file))
            else:
                print("File already exists: " + str(txt_file))
        
        pdftotext_file = open(txt_file, 'r')
        output_file = open(path+'_TXT/'+str(Path(os.path.basename(pdf_file)).stem)+'.txt', 'w+')
        
        
        output_file.write(os.path.basename(pdf_file).replace(' ', '_') + '\n')
    
        title = pdftotext_file.readline().strip()+pdftotext_file.readline().strip()
        output_file.write(title + '\n')

        output_file.write(abstract.readAbstract(pdftotext_file))

        pdftotext_file.close()
        output_file.close()
        os.remove(txt_file)


            
main()

'''

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

'''


