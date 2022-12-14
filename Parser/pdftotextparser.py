#!/usr/bin/python

import os
import subprocess
import argparse
from pathlib import Path

import abstract

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
        createFiles(path, "xml")
    elif args.txt:
        createFiles(path, "txt")
    else:
        print("Error: no output format specified")
        exit(1)
    


''''''''''''''''''
''' TEMP FILES '''
''''''''''''''''''

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


''''''''''''''
''' OUTPUT '''
''''''''''''''

def createFiles(inputPath, format):
    outputPath = inputPath + "_" + format.upper()
    SanitizeDirectory(outputPath)
    generateTempFiles(inputPath, outputPath)
    match format:
        case "xml":
            generateXMLFiles(outputPath)
        case "txt":
            generateTXTFiles(outputPath)
    cleanTempFiles(outputPath)
    exit(0)

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
        
        output_file.write(abstract.getReference(pdftotext_file))

        pdftotext_file.close()
        output_file.close()
        os.remove(outputPath+"/"+file)
    
    return

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

main()







