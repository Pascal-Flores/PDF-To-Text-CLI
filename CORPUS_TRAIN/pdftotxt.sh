#!/bin/bash

# This script converts all PDF files in a directory to text files
# using pdftotext. It is assumed that pdftotext is in the path.

# Usage: pdftotext.sh <directory>

#write the script here
for file in *.pdf ; do
    pdftotext -raw "$file"
done