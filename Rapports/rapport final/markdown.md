---
lang: fr
version: 1.0
date: 16/12/2022
documentclass: article
papersize: a4

title: Élaboration d'un utilitaire d'extraction de données à partir de sources scientifiques au format PDF (Portable Document Format)
author: 
- Pascal Flores
- Sébastien Ré
- Abdelouahed Kanouni

link-citations: true
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
references:
- id: pandoc
  language: en
  type: webpage
  title: Le site officiel de Pandoc
  author: John MacFarlane
  issued: 
    year: 2022
    month: 8
    day: 22
  URL: https://pandoc.org/index.html
  license : GPL



mainfont: scholax
header-includes:
  - \usepackage{filecontents}
  - \usepackage{fullpage}
  - \renewcommand{\listfigurename}{Table des illustrations}
  - \renewcommand{\contentsname}{Table des matières}
output:
  pdf_document:
    md_extensions: +grid_tables
fontsize: 12pt
---


# Abstract

Dans le cadre de la formation de License du CERI situé à Avignon, il a été demandé, lors des travaux pratiques du module de génie logiciel, de développer un outil d'extraction de données basé sur pdftotext, un outil de conversion de fichiers PDF en fichiers textes. \
L'objectif de ce projet est plutôt la mise en pratique du cours que le développement en lui-même, en mettant en place la méthodologie de travail appelée SCRUM. \
Nous verrons au travers de ce rapport la méthode de travail mise en place, les résultats obtenus et les difficultés rencontrées. \ 

# Méthode

## Environnement de développement

Pour travailler dans meilleures conditions et développer efficacement, nous avons choisi de développer notre outil en Python, pour sa facilité d'utilisation et sa grande polyvalence. \
Nous avons également choisi d'utiliser Github pour la gestion de version. \ 
Pour la rédaction de ce rapport, nous avons utilisé le langage de balisage Markdown, ensuite converti en lateX puis en PDF grâce à l'outil Pandoc @pandoc qui est un langage de balisage léger, facile à utiliser et qui permet de générer des documents de qualité. \

## L'outil pdftotext

Pdftotext est un outil de conversion de fichiers PDF en fichiers textes disponible sur la plupart des systèmes d'exploitation. Il est possible de l'utiliser en ligne de commande ou en tant que bibliothèque, et dispose d'une variété d'options qui le rendent très polyvalent. \
Afin de pouvoir extraire les données des fichiers PDF à traiter, nous avons ainsi utilisé pdftotext pour convertir les fichiers PDF en fichiers textes, afin d'ensuite en extraite les données intéressantes. \

## Notre outil

Notre outil, appelé sobrement la "MOAI" (pour Machine à Obtentir Admirablement des Informations), lorsqu'il est lancé, prend comme paramètres les options suivantes :

  + -t (--txt) ou -x (--xml) ou --xml-plus, qui permet de spécifier le format de sortie, avec respectivement une sortie texte, une sortie XML ou une sortie XML avec des balises supplémentaires  
  + Le chemin vers le dossier contenant les fichiers PDF à traiter 

La MOAI demande alors à l'utilisateur quels sont les fichiers PDF à traiter dans le dossier spécifié, en lui demandant d'entrer le numéro de chaque fichier à traiter, séparés par des virgules. \
Une fois les fichiers sélectionnés, la MOAI convertit les fichier PDF en fichiers textes temporaires grâce à pdftotext, puis récupère les données dont nous avons besoin, soit le nom du fichier d'origine, le titre de l'article, les auteurs, le résumé de l'article, et la bibliographie de l'article. Dans le cas de l'utilisation --xml-plus, la MOAI récupère également l'introduction, le corps, la conclusion et la discussion de l'article. \
Les fichiers de sortie sont ensuite stockées dans un dossier nommé de la même manière que le dossier d'entrée, mais accompagné du suffixe "_XML" ou "_TXT" selon le format choisi. \
La MOAI supprime finalemet les fichiers temporaires créés. \


# Résultats

# Conclusion

Grâce aux résultats obtenus, nous pouvons dire que la MOAI convertit assez bien les fichiers d'entrée qui lui sont présentés, au vu du temps de développement qui lui a été consacré. \
Bien sûr, l'outil n'est pas parfait, et ne parvient pas à détecter certaines parties du texte, notamment quand ces dernières ne sont pas délimitée par des mots-clé. \
Cette approximation est en partie dûe à l'utilisation de pdftotext, qui s'il permet rapidement d'accéder aux contenus des articles, fait perdre toutes les informations sur le formatage du texte d'origine (mots en gras, italique, sauts de plusieurs lignes, etc...), qui auraient pu être utiles pour la détection des différentes parties, comme du titre de l'article et de la liste des auteurs notamment. \
Il aurait peut-être été plus long, mais plus gratifiant, de devoir décrypter le fichier PDF nous-même, afin de pouvoir en extraire toutes les informations sémantiques de mise en page. \

# Bibliographie
