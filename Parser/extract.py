
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
        self.fileString = pdftotext_file.read().splitlines()# list of lines  
        
    """ 
    Description: Trouve le prochain titre dans le fichier en fonction de la liste des titres passés en paramètre
    Arg : liste des titres à chercher, liste de string, ex: ["Introduction", "Conclusion"], si [""], alors le prochain titre est le suivant
    return : numéro de ligne correspondant au titre voulu
    """
    def getNextTitle(self, titles):
        
        nextTitle = False
        for line in self.fileString:
            for title_name in titles:
                if title_name == "":
                    nextTitle = True
                #si il trouve chiffre romain regex premier mot & title_name.upper() in line.upper(): ou
                if  len(re.findall("^[IVXLCDM]+\.?\s", line)) and (title_name.upper() in line.upper() or nextTitle):
                    #pour tout les mots de la ligne
                    for word in line.split():
                        #si la premiere lettre est une majuscule
                        if word[0].isupper():
                            return self.fileString.index(line)
                
                #si il trouve chiffre arabes regex & title_name.upper() in line.upper(): ou
                if len(re.findall("^[0-9]+\.?\s", line)) and (title_name.upper() in line.upper() or nextTitle):
                    #pour tout les mots de la ligne
                    for word in line.split():
                        #si la premiere lettre est une majuscule
                        if word[0].isupper():
                            return self.fileString.index(line)
                
                if "conclusion".upper() == title_name.upper() or nextTitle:
                    continue
                if len(re.findall("^"+title_name.upper(), line.upper() )) and line[0].isupper():#si il trouve le titre
                    self.typeTitre = "-"
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
        
        return txt+" "+self.fileString.pop(0)

    """
    Description: Récupère les auteurs de l'article
    return : auteurs de l'article
    """
    def getAuthors(self):
        num = self.getNextTitle(["ABSTRACT"])#on cherche le prochain titre qui est abstract
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)
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
            ret += self.fileString.pop(0)
        return ret

    """
    Description: Récupère l'introduction de l'article
    return : introduction de l'article
    """
    def getIntroduction(self):
        ret = ""
        ret += self.fileString.pop(0)#on retire le titre introduction
        num = self.getNextTitle([""])#on cherche le prochain titre
        for i in range(num):
            ret += self.fileString.pop(0)
        return ret

    """
    Description: Récupère le corps de l'article
    return : corps de l'article
    """
    def getCorps(self):
        num = self.getNextTitle(["conclusion","Discussion"])#on cherche le prochain titre qui est conclusion ou discussion
        if num == -1: 
            num = self.getNextTitle(["Reference"])#si pas de conclusion ou discussion, on prend le prochain titre qui est reference
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)
        return ret
        
    """
    Description: Récupère la conclusion de l'article
    return : conclusion de l'article
    """
    def getConclusion(self, arg):
        num = self.getNextTitle(arg)#on cherche le/les prochains titre(s) qui est/sont dans arg
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)
        return ret

    """
    Description: Récupère la discussion de l'article
    return : discussion de l'article
    """
    def getDiscussion(self, arg):
        num = self.getNextTitle(arg)#on cherche le/les prochains titre(s) qui est/sont dans arg
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)
        return ret
    
    """
    Description: Récupère les références de l'article (toutes les lignes jusqu'à la fin du fichier)
    return : références de l'article
    """
    def getReference(self):
        num = 0
        ret = ""
        while num < len(self.fileString):
            ret += self.fileString.pop(0)
            num+=1
        return ret