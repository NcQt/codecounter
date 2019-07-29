#!/usr/bin/env python

# This Python script counts the lines of code in the directory in which it is
# run.  It only looks at files which end in the file extensions passed to the
# script as arguments.

# It outputs counts for total lines, blank lines, comment lines and code lines
# (total lines minus blank lines and comment lines).

# Example usage and output:
# > lines_of_code_counter.py workDir .h .cpp
# Total lines:   15378
# Blank lines:   2945
# Comment lines: 1770
# Code lines:    10663

# Change this value based on the comment symbol used in your programming
# language.
commentSymbol = "//"

import sys
import os, os.path
import chardet

workDir = sys.argv[1]
acceptableFileExtensions = sys.argv[2:]
if not acceptableFileExtensions:
    print('Please pass at least one file extension as an argument.')
    quit()


filesToCheck = []
for root, _, files in os.walk(workDir):
    for f in files:
        fullpath = os.path.join(root, f)
        if '.git' not in fullpath:
            for extension in acceptableFileExtensions:
            	if fullpath.endswith(extension):
                    filesToCheck.append(fullpath)

if not filesToCheck:
    print ('No files found.')
    quit()

lineCount = 0
totalBlankLineCount = 0
totalCommentLineCount = 0

print ('')
print('%-40s%15s%15s%15s%15s' % ('Filename','lines','blank lines','comment lines','code lines'))
#print ('Filename\tlines\tblank lines\tcomment lines\tcode lines')

for fileToCheck in filesToCheck:
    filedata = open(fileToCheck, 'rb')
    data = filedata.read()
    fileEncoding = chardet.detect(data).get("encoding")
    if fileEncoding is None:
        continue
    with open(fileToCheck,encoding=fileEncoding) as f:

        fileLineCount = 0
        fileBlankLineCount = 0
        fileCommentLineCount = 0

        for line in f:
            lineCount += 1
            fileLineCount += 1

            lineWithoutWhitespace = line.strip()
            if not lineWithoutWhitespace:
                totalBlankLineCount += 1
                fileBlankLineCount += 1
            elif lineWithoutWhitespace.startswith(commentSymbol):
                totalCommentLineCount += 1
                fileCommentLineCount += 1

        print ('%-40s%15s%15s%15s%15s' % \
              (os.path.basename(fileToCheck), \
              str(fileLineCount), \
              str(fileBlankLineCount), \
              str(fileCommentLineCount), \
              str(fileLineCount - fileBlankLineCount - fileCommentLineCount)))


print ('')
print ('Totals')
print ('--------------------')
print ('Lines         : ' + str(lineCount))
print ('Blank lines   : ' + str(totalBlankLineCount))
print ('Comment lines : ' + str(totalCommentLineCount))
print ('Code lines:   : ' + str(lineCount - totalBlankLineCount - totalCommentLineCount))