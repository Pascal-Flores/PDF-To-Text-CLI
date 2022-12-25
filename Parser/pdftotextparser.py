#!/usr/bin/python

import os
import subprocess
import argparse
from pathlib import Path

import abstract

def main():    
    parser = argparse.ArgumentParser()#argument parser
    parser.add_argument("path", help="path to the directory containing the pdf files")#argument path
    parser.add_argument("-x", "--xml", action="store_true",  help="output file will be in xml format")#argument xml
    parser.add_argument("-t", "--txt", action="store_true", help="output file will be in txt format")#argument txt

    args = parser.parse_args()#parse les arguments

    path = args.path#path prend la valeur de l'argument path
    if args.xml and args.txt:#si les deux arguments sont présents
        print("Error: cannot specify both xml and txt output")
        exit(1)
    elif args.xml:#si l'argument xml est présent
        createFiles(path, "xml")
    elif args.txt:#si l'argument txt est présent
        createFiles(path, "txt")
    else:#si aucun argument n'est présent
        print("Error: no output format specified")
        exit(1)
        
    
    


''''''''''''''''''
''' TEMP FILES '''
''''''''''''''''''

def SanitizeOutputDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.listdir(path):
        for file in os.listdir(path):
            os.remove(path+"/"+file)

def generateTempFiles(inputPath, outputPath, files):
    for file in files:
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

    print("Please select the files you want to parse:")
    i = 0
    for file in os.listdir(inputPath):
        if file.endswith(".pdf"):
            print(str(i)+'. '+file)
            i += 1
    print("Enter the number of the files you want to parse, separated by a space:")
    filesIndexes = input().split()
    files = []
    i = 0
    for file in os.listdir(inputPath):
        if file.endswith(".pdf"):
            if str(i) in filesIndexes:
                files.append(file)
            i += 1

    outputPath = inputPath + "_" + format.upper()#outputPath prend la valeur de l'argument path + _ + xml ou txt
    SanitizeOutputDirectory(outputPath)#nettoie le dossier de sortie
    generateTempFiles(inputPath, outputPath, files)#génère les fichiers temporaires
    match format:#match le format
        case "xml":
            generateXMLFiles(outputPath, files)
        case "txt":
            generateTXTFiles(outputPath, files)
    cleanTempFiles(outputPath)
    exit(0)

def generateTXTFiles(outputPath, files):
    for file in os.listdir(outputPath):
        if not file.endswith(".pdf.txt"):
            continue
        else:
            pdftotext_file = open(outputPath+"/"+file, 'r')

        input_file_name = Path(os.path.basename(file)).stem

        output_file = open(outputPath+"/"+Path(input_file_name).stem+".txt", 'w+')
        
        output_file.write(abstract.getPreamble(input_file_name) + '\n')
        output_file.write(abstract.getTitle(pdftotext_file) + '\n')
        output_file.write(abstract.getAuthors(pdftotext_file) + '\n')
        output_file.write(abstract.readAbstract(pdftotext_file) + '\n')
        output_file.write(abstract.getIntroduction(pdftotext_file) + '\n')
        output_file.write(abstract.getCorps(pdftotext_file) + '\n')
        output_file.write(abstract.getConclusion(pdftotext_file) + '\n')
        output_file.write(abstract.getDiscussion(pdftotext_file) + '\n')
        output_file.write(abstract.getReference(pdftotext_file) + '\n')

        pdftotext_file.close()
        output_file.close()
    
    return

def generateXMLFiles(outputPath, files):
    for file in os.listdir(outputPath):
        if not file.endswith(".pdf.txt"):
            continue
        else:
            pdftotext_file = open(outputPath+"/"+file, 'r')
        input_file_name = Path(os.path.basename(file)).stem
        output_file = open(outputPath+"/"+Path(input_file_name).stem+".xml", 'w+')

        extracter = abstract.extract(pdftotext_file)
        output_file.write('<article>\n')
        output_file.write("\t<preamble>" + extracter.getPreamble(input_file_name) + '</preamble>\n')
        output_file.write("\t<title>"+ extracter.getTitle() + '</title>\n')
        output_file.write("\t<authors>" + extracter.getAuthors() + '</authors>\n')
        output_file.write("\t<abstract>"+extracter.getAbstract()+"</abstract>\n")
        output_file.write("\t<introduction>"+extracter.getIntroduction()+"</introduction>\n")
        output_file.write("\t<corps>"+extracter.getCorps()+"</corps>\n")
        output_file.write("\t<conclusion>"+extracter.getConclusion()+"</conclusion>\n")
        output_file.write("\t<discussion>"+extracter.getDiscussion()+"</discussion>\n")
        output_file.write("\t<biblio>"+extracter.getReference()+"</biblio>\n")
        output_file.write('</article>\n')

        pdftotext_file.close()
        output_file.close()
    
    return

main()




