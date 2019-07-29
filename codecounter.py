"""
.. usage:

   codecounter.py <basedir> <whitelist>
   where <basedir> refers to a path for the counter files.

   Example: python codecounter.py E:\code m 
"""

import os
import time
import chardet
import sys

# basedir = 'E:\\code\\matlab'
filelists = []
# 指定想要统计的文件类型
# whitelist = ['m','xml']

#遍历文件, 递归遍历文件夹中的所有


def getFile(basedir):
    global filelists
    for parent, dirnames, filenames in os.walk(basedir):
        # for dirname in dirnames:
        #    getFile(os.path.join(parent,dirname)) #递归
        for filename in filenames:
            ext = filename.split('.')[-1]
            # 只统计指定的文件类型，略过一些log和cache文件
            if ext in whitelist:
                filelists.append(os.path.join(parent, filename))

# 统计一个文件的行数


def countLine(fname):
    count = 0
    filedata = open(fname, 'rb')
    data = filedata.read()
    fileEncoding = chardet.detect(data).get("encoding")
    if fileEncoding is None:
        return count

    filedata = open(fname, 'r', encoding=fileEncoding)

    for file_line in filedata.readlines():
        if file_line != '' and file_line != '\n':  # 过滤掉空行
            count += 1
    print('%-40s ---- %-5d' % (os.path.basename(fname), count))
    return count


if __name__ == '__main__':
    basedir = sys.argv[1]
    whitelist = sys.argv[2:]

    startTime = time.clock()
    getFile(basedir)
    totalline = 0
    for filelist in filelists:
        totalline = totalline + countLine(filelist)
    print('total lines:', totalline)
    print('Done! Cost Time: %0.2f second' % (time.clock() - startTime))
