#!/usr/bin/python

import os
import subprocess
import argparse
from pathlib import Path

import extract

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
    outputPath = inputPath + "_" + format.upper()#outputPath prend la valeur de l'argument path + _ + xml ou txt
    SanitizeOutputDirectory(outputPath)#nettoie le dossier de sortie
    generateTempFiles(inputPath, outputPath)#génère les fichiers temporaires
    match format:#match le format
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
        
        extracter = extract.extract(pdftotext_file)
        output_file.write("Préamble :\n\t" + extracter.getPreamble(input_file_name))
        output_file.write("\nTitre :\n\t"+ extracter.getTitle())
        output_file.write("\nAuteurs :\n\t" + extracter.getAuthors())
        output_file.write("\nAbstract :\n\t"+extracter.getAbstract())
        output_file.write("\nIntroduction :\n\t"+extracter.getIntroduction())
        output_file.write("\nCorps :\n\t"+extracter.getCorps())
        if "CONCLUSION" in extracter.fileString[extracter.getNextTitle(["Conclusion","Discussion"])]:
            output_file.write("\nConclusion :\n\t"+extracter.getConclusion(["Discussion","references"]))
            output_file.write("\nDiscussion :\n\t"+extracter.getDiscussion(["references"]))
        else : #Discussion
            output_file.write("\nDiscussion :\n\t"+extracter.getDiscussion(["Conclusion","references"]))
            output_file.write("\nConclusion :\n\t"+extracter.getConclusion(["References"]))
            
        output_file.write("\nBiblio :\n\t"+extracter.getReference())

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
        output_file = open(outputPath+"/"+Path(input_file_name).stem+".xml", 'w+')
        print (output_file.name)

        extracter = extract.extract(pdftotext_file)
        output_file.write('<article>\n')
        output_file.write("\t<preamble>" + extracter.getPreamble(input_file_name) + '</preamble>\n')
        output_file.write("\t<title>"+ extracter.getTitle() + '</title>\n')
        output_file.write("\t<auteur>" + extracter.getAuthors() + '</auteur>\n')
        output_file.write("\t<abstract>"+extracter.getAbstract()+"</abstract>\n")
        output_file.write("\t<introduction>"+extracter.getIntroduction()+"</introduction>\n")
        output_file.write("\t<corps>"+extracter.getCorps()+"</corps>\n")
        if "CONCLUSION" in extracter.fileString[extracter.getNextTitle(["Conclusion","Discussion"])]:
            output_file.write("\t<conclusion>"+extracter.getConclusion(["Discussion","references"])+"</conclusion>\n")
            output_file.write("\t<discussion>"+extracter.getDiscussion(["references"])+"</discussion>\n")
        else : #Discussion
            output_file.write("\t<discussion>"+extracter.getDiscussion(["Conclusion","references"])+"</discussion>\n")
            output_file.write("\t<conclusion>"+extracter.getConclusion(["References"])+"</conclusion>\n")
            
        output_file.write("\t<biblio>"+extracter.getReference()+"</biblio>\n")
        output_file.write('</article>')

        pdftotext_file.close()
        output_file.close()
        os.remove(outputPath+"/"+file)
    
    return

main()




