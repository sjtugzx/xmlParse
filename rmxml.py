import os
import glob

if __name__ == '__main__':

    path = 'data/'
    print("删除文件：")
    print("-------------------")
    for infile in glob.glob(os.path.join(path, '*.xml')):
        os.remove(infile)