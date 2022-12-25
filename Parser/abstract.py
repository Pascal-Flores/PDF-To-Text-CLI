

import os
import sys
import re
import string

corpus = "CORPUS_TRAIN"
filename = "*.txt"
TWOCOLS = True
 
class extract():
    def __init__(self, pdftotext_file):
        self.fileString = pdftotext_file.read().splitlines()# list of lines  
        
    def getNextTitle(self, title_name):
        #
        nextTitle = False
        if title_name == "":
            nextTitle = True
        for line in self.fileString:
            
            #si il trouve chiffre romain regex premier mot & title_name.upper() in line.upper(): ou
            if  len(re.findall("^[IVXLCDM]* ", line)) and (title_name.upper() in line.upper() or nextTitle):
                return self.fileString.index(line)
            
            #si il trouve chiffre arabes regex & title_name.upper() in line.upper(): ou
            if len(re.findall("^[0-9]", line)) and (title_name.upper() in line.upper() or nextTitle):
                #pour tout les mots de la ligne
                for word in line.split():
                    #si la premiere lettre est une majuscule
                    if word[0].isupper():
                        return self.fileString.index(line)
            
            if "conclusion".upper() == title_name.upper() or nextTitle:
                continue
            if len(re.findall("^"+title_name.upper(), line.upper() )):#si title_name est le premier mot de la ligne
                return self.fileString.index(line)
            
        return -1
        
    def getPreamble(self, input_file_name):
        return input_file_name.replace(' ', '_')              

    def getTitle(self):
        # trier avec regex xx/xx et 4chffres d'affilés xx-xx
        txt = ""
        while txt == "":
            txt = self.fileString.pop(0)
            x = re.findall("[0-9]", txt)
            if len(txt) < 6:
                txt = ""
            if len(x) > 1:#si pas de chiffre
                txt = ""
        
        return txt+" "+self.fileString.pop(0)

    def getAuthors(self):
        num = self.getNextTitle("ABSTRACT")
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)
        return ret
    
    def getAbstract(self):
        num = self.getNextTitle("INTRODUCTION")
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

    def getIntroduction(self):
        num = self.getNextTitle("WORK ")
        if num == -1: 
            num = self.getNextTitle(" Method ")
            if num == -1:
                num = self.getNextTitle("")
            
        print(self.fileString[num])
        
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret


    def getCorps(self):
        num = self.getNextTitle("conclusion")
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret
        

    def getConclusion(self):
        return "not implemented yet"

    def getDiscussion(self):
        return "not implemented yet"

    def getReference(self):
        num = self.getNextTitle("REFERENCES")
        ret = ""
        while num < len(self.fileString):
            ret += self.fileString.pop(num)
            num+=1
        return ret