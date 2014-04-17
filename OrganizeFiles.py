#!/usr/bin/python
# Organize Files Script
# If file count > 100, put 100 files in sub dir.

import sys
import os
import shutil

def getsubpath(filepath):
    isfindpath = False
    pathnum = 1
    while isfindpath == False:
        subpath = os.path.join(filepath, str(pathnum))
        if os.path.exists(subpath) == False:
            os.mkdir(subpath)
            isfindpath = True
            return subpath
        pathnum = pathnum + 1

def main():
    filelist = []
    filecount = 100
    filepath = os.getcwd()
    selffilename = 'OrganizeFiles.py'

    # Get file list
    v = os.walk(filepath)
    for root, dirs, files in v:
        filelist = files
        break

    # Exclude self file
    filelist.remove(selffilename)

    i = 1
    while filecount * i < len(filelist):
        # get sub path's files
        subfilelist = filelist[(i-1)*filecount:i*filecount]
        subpath = getsubpath(filepath)
        # move files
        for f in subfilelist:
            shutil.move(os.path.join(filepath, f), os.path.join(subpath, f))
        i = i + 1

if __name__ == '__main__':
    main()