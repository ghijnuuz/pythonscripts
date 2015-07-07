# compressor.py
# version 1.0

import os
import sys
import subprocess

yuicompressorfile = "yuicompressor-2.4.8.jar"

def findfile(dirpath):
    result = { "js": [], "css": [] }
    print(dirpath)
    for root, dirs, files in os.walk(dirpath):
        for fileitem in files:
            if os.path.splitext(fileitem)[1] == ".js":
                filefullname = os.path.join(root, fileitem)
                result["js"].append(filefullname)
            if os.path.splitext(fileitem)[1] == ".css":
                filefullname = os.path.join(root, fileitem)
                result["css"].append(filefullname)
    return result

def compressor(filelist):
    for f in filelist:
    	print("Compressor " + f)
    	cmd = "java -jar \"" + yuicompressorfile + "\" -o '.js$:.js' " + f
    	subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    yuicompressorfile = os.path.join(sys.path[0], yuicompressorfile)
    dirpath = ""
    if len(sys.argv) > 1:
        dirpath = sys.argv[1]
    else:
        dirpath = os.getcwd()
    if os.path.isdir(dirpath):
        result = findfile(dirpath)
        print("Find " + str(len(result["js"])) + " js files, " + str(len(result["css"])) + " css files.")
        compressor(result["js"])
        compressor(result["css"])
    else:
        print("It's not path.")
    print("Press Enter to exit.")
    try:
        raw_input()
    except:
        input()