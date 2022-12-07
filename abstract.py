

import os
import sys
import re
import string

corpus = "CORPUS_TRAIN"
filename = "*.txt"
TWOCOLS = True

def main():
    for filename in os.listdir(corpus):
        ouverturefichier(os.path.join(corpus, filename))
        print("")

def ouverturefichier(filename):
    if filename.endswith(".txt"):
        # on ouvre le fichier
        print(filename)
        f = open(filename, 'r')
        print(readAbstract(f))
        # on ferme le fichier
        f.close()

def readAbstract(f):
    content = []
    lastLine = "-"
    for line in f:
        line = line.strip()
        content.append(line)
        if line[0].isupper() and lastLine[-1] != ".":
            #si la ligne commence par une majuscule et que la ligne précédente ne se termine pas par un point
            firstLine = line
        if "INTRODUCTION" in line.upper():#si on trouve le mot introduction
            break
        lastLine = line

    ret = []
    start = False
    for line in content:
        if firstLine == line or "ABSTRACT" in line.upper() :
            start = True
        if start:
            ret.append(line)
        if lastLine == line :
            break
    
    return " ".join(ret)
    
    

        
main()