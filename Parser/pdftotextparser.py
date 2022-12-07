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
    parser.add_argument("-x", "--xml", action="store_true",  help="output file will be in xml format")
    parser.add_argument("-t", "--txt", action="store_true", help="output file will be in txt format")

    args = parser.parse_args()

    path = args.path
    if args.xml and args.txt:
        print("Error: cannot specify both xml and txt output")
        exit(1)
    elif args.xml:
        outputFilesInXMLFormat(path)
    elif args.txt:
        outputFilesInTXTFormat(path)

def SanitizeDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.listdir(path):
        for file in os.listdir(path):
            os.remove(path+"/"+file)

def generateTempFiles(inputPath, outputPath):
    for file in os.listdir(inputPath):
        if file.endswith(".pdf"):
            pdf_file = Path(inputPath + "/" + file)
            txt_file = Path(outputPath+ "/" + file + ".txt")
            if not txt_file.is_file():
                subprocess.call(["pdftotext", "-raw", pdf_file, txt_file])
                print ("Created temporary text file: " + str(txt_file))
            else:
                print("File already exists: " + str(txt_file))
    return

def cleanTempFiles(path):
    for file in os.listdir(path):
        if file.endswith(".pdf.txt"):
            os.remove(path+"/"+file)

def outputFilesInXMLFormat(inputPath):
    outputPath = inputPath + "_XML"
    SanitizeDirectory(outputPath)
    generateTempFiles(inputPath, outputPath)
    
    cleanTempFiles(outputPath)
    print("xml output not yet implemented")
    exit(1)

''''''''''''''''''
''' TXT OUTPUT '''
''''''''''''''''''

def generateTXTFiles(outputPath):
    for file in os.listdir(outputPath):
        print(file)
        if not file.endswith(".pdf.txt"):
            continue
        else:
            pdftotext_file = open(outputPath+"/"+file, 'r')

        input_file_name = Path(os.path.basename(file)).stem

        output_file = open(outputPath+"/"+Path(input_file_name).stem+".txt", 'w+')
        print (output_file.name)
        output_file.write(input_file_name.replace(' ', '_') + '\n')
    
        title = pdftotext_file.readline().strip()+pdftotext_file.readline().strip()
        output_file.write(title + '\n')

        output_file.write(abstract.readAbstract(pdftotext_file))

        pdftotext_file.close()
        output_file.close()
        os.remove(outputPath+"/"+file)
    
    return

def outputFilesInTXTFormat(inputPath):
    outputPath = inputPath + "_TXT"
    SanitizeDirectory(outputPath)
    generateTempFiles(inputPath, outputPath)
    generateTXTFiles(outputPath)
    cleanTempFiles(outputPath)

def generateFiles(inputPath, format):
    match format:
        case "xml":
            outputPath = inputPath + "_XML"
        case "txt":
            outputPath = inputPath + "_TXT"
        case _:
            print("Error: invalid format")
            exit(1)
    
    SanitizeDirectory(outputPath)
    generateTempFiles(inputPath, outputPath)
    match format:
        case "xml":
            generateXMLFiles(outputPath)
        case "txt":
            generateTXTFiles(outputPath)
        
    cleanTempFiles(outputPath)

main()





def generateXMLFiles(outputPath):
    for file in os.listdir(outputPath):
        print(file)
        if not file.endswith(".pdf.txt"):
            continue
        else:
            pdftotext_file = open(outputPath+"/"+file, 'r')

        input_file_name = Path(os.path.basename(file)).stem

        output_file = open(outputPath+"/"+Path(input_file_name).stem+".txt", 'w+')
        print (output_file.name)

        # 
        output_file.write(input_file_name.replace(' ', '_') + '\n')
    
        title = pdftotext_file.readline().strip()+pdftotext_file.readline().strip()
        output_file.write(title + '\n')

        output_file.write(abstract.readAbstract(pdftotext_file))

        pdftotext_file.close()
        output_file.close()
        os.remove(outputPath+"/"+file)
    
    return



