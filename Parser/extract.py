
import os
import sys
import re
import string

"""
Description: Classe qui permet d'extraire les informations d'un fichier texte
possède une variable d'objet fileString qui est une liste de string qui contient toutes les lignes du fichier
on supprime petit à petit les lignes en les récupérant dans les fonctions
ainsi donc nous somme CERTAINS de ne pas avoir de doublons et de ne pas perdre d'informations !
chaque fonction correspond à chaque partie du document ainsi voulus
"""
class extract():
    
    def __init__(self, pdftotext_file):
        self.type = "txt"
        self.fileString = pdftotext_file.read().splitlines()# list of lines  
        
    """ 
    Description: Trouve le prochain titre dans le fichier en fonction de la liste des titres passés en paramètre
    Arg : liste des titres à chercher, liste de string, ex: ["Introduction", "Conclusion"], si [""], alors le prochain titre est le suivant
    return : numéro de ligne correspondant au titre voulu
    """
    def getNextTitle(self, titles):
        nextTitle = False
        last = ""
        for line in self.fileString:
            for title_name in titles:
                if title_name == "":
                    nextTitle = True
                #si il trouve chiffre romain regex premier mot & title_name.upper() in line.upper(): ou
                if  len(re.findall("^[IVXL]+\.?\s", line)) and (len(re.findall("\s{}".format(title_name.upper()), line.upper() )) or nextTitle) and (self.type != "arabe" and self.type != "arabePoint"):
                    #pour tout les mots de la ligne
                    i = 0
                    for word in line.split():
                        #si la premiere lettre est une majuscule
                        if word[0].isupper() and i >= 1:
                            if re.findall("^[IVXL]+\.$", line.split()[0]) and self.type != "roman": 
                                self.type = "romanPoint"
                            elif re.findall("^[IVXL]+$", line.split()[0]) and self.type != "romanPoint":
                                self.type = "roman"
                            else :
                                continue
                            return self.fileString.index(line)
                        i += 1
                
                #si il trouve chiffre arabes regex & title_name.upper() in line.upper(): ou
                if len(re.findall("^[0-9]+\.?[0-9]*\s", line)) and (len(re.findall("\s{}".format(title_name.upper()), line.upper())) or nextTitle) and (self.type != "roman" and self.type != "romanPoint"):
                    #pour tout les mots de la ligne
                    i = 0
                    for word in line.split():
                        #si la premiere lettre est une majuscule
                        if word[0].isupper() and i >= 1:
                            if re.findall("^[0-9]+\.$", line.split()[0]) and self.type != "arabe": 
                                self.type = "arabePoint"
                            elif re.findall("^[0-9]+$", line.split()[0]) and self.type != "arabePoint":
                                self.type = "arabe"
                            else :
                                continue
                            return self.fileString.index(line)
                        i += 1
                
                if "conclusion".upper() == title_name.upper() or nextTitle:
                    continue
                if len(re.findall("^"+title_name.upper(), line.upper().replace(" ","") )) and self.type == "txt":#si il trouve le titre
                    return self.fileString.index(line)
                    
            
        return -1
     
    """
    return : nom du fichier avec des _ à la place des espaces
    """   
    def getPreamble(self, input_file_name):
        return input_file_name.replace(' ', '_')              

    """
    Description: Récupère le titre de l'article
    supprime les lignes du début du fichier jusqu'au titre
    return : titre de l'article
    """
    def getTitle(self):
        txt = ""
        while txt == "":
            txt = self.fileString.pop(0)
            x = re.findall("[0-9]", txt)
            if len(txt) < 6:
                txt = ""
            if len(x) > 1:#si pas de chiffre
                txt = ""
            x = re.findall("THIS", txt.upper())
            if len(x) > 0:#si pas de this
                txt = ""
        
        return txt+" "+self.fileString.pop(0)

    """
    Description: Récupère les auteurs de l'article
    return : auteurs de l'article
    """
    def getAuthors(self):
        num = self.getNextTitle(["ABSTRACT"])#on cherche le prochain titre qui est abstract
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret
    
    """
    Description: Récupère l'abstract de l'article
    return : abstract de l'article
    """
    def getAbstract(self):
        num = self.getNextTitle(["INTRODUCTION"])#on cherche le prochain titre qui est introduction
        if num == -1: 
            num = self.getNextTitle([""])#si pas d'introduction, on prend le prochain titre
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

    """
    Description: Récupère l'introduction de l'article
    return : introduction de l'article
    """
    def getIntroduction(self):
        ret = ""
        ret += self.fileString.pop(0)+" "#on retire le titre introduction
        num = self.getNextTitle(["work"])
        if num == -1:
            num = self.getNextTitle([""])#on cherche le prochain titre
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

    """
    Description: Récupère le corps de l'article
    return : corps de l'article
    """
    def getCorps(self):
        num = self.getNextTitle(["conclusion","Discussion"])#on cherche le prochain titre qui est conclusion ou discussion
        if num == -1: 
            num = self.getNextTitle(["Final"])#si pas de conclusion ou discussion, on prend le prochain titre qui est final
            if num == -1:
                num = self.getNextTitle(["Reference"])#si pas de conclusion ou discussion, pas de final on prend le prochain titre qui est reference
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret
        
    """
    Description: Récupère la conclusion de l'article
    return : conclusion de l'article
    """
    def getConclusion(self, arg):
        self.type = "txt"
        num = self.getNextTitle(arg)#on cherche le/les prochains titre(s) qui est/sont dans arg
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

    """
    Description: Récupère la discussion de l'article
    return : discussion de l'article
    """
    def getDiscussion(self, arg):
        self.type = "txt"
        num = self.getNextTitle(arg)#on cherche le/les prochains titre(s) qui est/sont dans arg
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret
    
    """
    Description: Récupère les références de l'article (toutes les lignes jusqu'à la fin du fichier)
    return : références de l'article
    """
    def getReference(self):
        num = self.getNextTitle(["REFERENCES"])
        if num == -1:
            num = self.getNextTitle([""])
        ret = ""
        while num < len(self.fileString):
            ret += self.fileString.pop(num)+" "
        return ret