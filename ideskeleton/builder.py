import os.path
def build(source_path, overwrite = True):
    if not os.path.exists(source_path):
        raise IOError("source_path does not exist so not skeleton can be built")
    '''
    for root, dirs, files in os.walk("."):
    path = root.split('/')
    print (len(path) - 1) *'---' , os.path.basename(root)       
    for file in files:
        print len(path)*'---', file
    '''