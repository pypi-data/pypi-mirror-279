# Run this file to install Lunarcord Beta.

import os, sys, shutil, site, pickle, pyperclip, zlib

data = b''

def getPythonVersion():
    
    '''
    Gets the current Python version that is being used to install Lunarcord, eg `311`
    '''

    versionInfo = sys.version_info
    versionMinor = versionInfo.minor
    versionMajor = versionInfo.major
    return str(versionMajor) + str(versionMinor)

def add(path1, *paths):
    
    '''
    Joins two or more paths and returns the result.
    '''
        
    return str(os.path.join(path1, *paths))
    
def getPythonDirectory(vname: str = None):
    
    '''
    Gets the directory in which Python should be installed in your computer, which is usually something like `Python311` where `311` is the version.
    '''
    
    vers = getPythonVersion() if vname is None else str(vname)
    
    name = 'Python' + vers
    
    path1 = os.path.join(
        'C:o',
        name
    )
    
    path2 = os.path.join(
        'c:o',
        name
    )
    
    path1 = path1.replace('o', '', 1)
    path2 = path2.replace('o', '', 1)
    
    if exists(path1):
        
        return path1, vers
    
    if exists(path2):
        
        return path2, vers
    
    return os.path.split(sys.executable)[0], vers

def exists(path: str):
    
    '''
    Returns whether the given file or directory exists.
    '''
    
    return os.path.exists(path)

def getPackages(pythonPath):
    
    '''
    Gets the path for all installed python libraries for the given `pythonPath`.
    '''
    
    path = add(
        pythonPath,
        'Lib',
        'site-packages'
    )
    
    if exists(path):
        return path
    
    try:
        pkgs = site.getsitepackages()
        return (pkgs[-1])
    
    except:
        return None


def getDist(version: str):
    
    '''
    Get the path for the appropriate Lunarcord distribution for Python version `version`.
    '''
    
    version = int(version)
    
    if version > 312:
        version = 312
    
    if version < 311:
        version = 311
        
    version = str(version)
    path = 'lunarcord-v' + version
    
    if not exists(path):
        return None
    
    return path

def compress(path: str):
    
    raw = {}
    
    for x in os.listdir(path):
        
        full = add(path, x)
        name = add('lunarcord', x)
        isFolder = os.path.isdir(full)
        isFile = os.path.isfile(full)
        
        if not isFile and not isFolder:
            
            continue
        
        if isFolder:
            
            data = compress(full)
            
        elif isFile:
            
            with open(full, 'rb') as reader:
                data = reader.read()
                
        raw[x] = data
        
    pickled = pickle.dumps(raw)
    pickled = zlib.compress(pickled, 9)
    #pyperclip.copy(str(pickled))
    return pickled
    
def decompress(raw: bytes, target: str):
    
    raw = zlib.decompress(raw)
    data: dict = pickle.loads(raw)
    
    final = add(target, 'lunarcord')
   
    if os.path.exists(final):
        shutil.rmtree(final)
        
    os.mkdir(final)
    
    for path in data:
        
        value = data.get(path)
        full = add(final, path)
        
        try:
            value = pickle.loads(zlib.decompress(value))
            isFolder = True
            
        except:
            isFolder = False
        
        if isFolder:
            
            os.mkdir(full)
            
            for sub in value:
                
                subfull = add(full, sub)
                subval = value.get(sub)
                
                with open(subfull, 'wb') as subwriter:
                    
                    subwriter.write(subval)
            
        else:
            
            with open(full, 'wb') as writer:
                
                writer.write(value)
        
        
        
data = compress('src/lunarcord')

VERSION = None

directory, version = getPythonDirectory(VERSION)

if not directory:
    
    print('[x] Failed to find Python directory!')
    
else:
    
    pkg = getPackages(directory)
    
    if not pkg:
        
        print('[x] Failed to find packages directory!')
        
    else:
        
        target = add(pkg, 'lunarcord')
        
        if exists(target):
             
            print('[!] Lunarcord has already been installed!')
            print('[-] Deleting previous installation...')
            shutil.rmtree(target)
        
        print('[+] Initializing installation...')
        
        #dist = getDist(version)
        dist = 'src/lunarcord'
        
        if dist is None:
            print('[x] Failed to get Lunarcord distribution!')
            
        else:
            
            print('[-] Installing Lunarcord...')
            decompress(data, pkg)
            print('[+] Lunarcord has been installed succesfully!')
            
            print('[-] Installation path:', target)