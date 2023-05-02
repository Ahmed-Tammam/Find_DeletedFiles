import os
import shutil
from winreg import *


def sidT0user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList" + '\\' + sid)
        (value, type) = QueryValueEx(key, "ProfileImagePath")
        user = value.split('\\')
        return user
    except:
        return sid


def returnDir():
    dir = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycled in dir:
        if os.path.isdir(recycled):
            return recycled
    return None


def findrecycled(recycled, dumpdir):
    if not os.path.exists(dumpdir):
        os.makedirs(dumpdir)
    dirlist = os.listdir(recycled)
    for sid in dirlist:
        files = os.listdir(recycled + sid)
        user = sidT0user(sid)
        print('\n[*] Dumping files for User: ' + str(user))
        for file in files:
            filepath = os.path.join(recycled, sid, file)
            newfilepath = os.path.join(dumpdir, file)
            shutil.move(filepath, newfilepath)
            print('[*] Dumped file: ' + newfilepath)


if __name__ == '__main__':
    recycled = returnDir()
    dumpdir = 'D:\\DumpedFiles\\'
    findrecycled(recycled, dumpdir)