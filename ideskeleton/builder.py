import os.path
def build(source_path, overwrite = True, ide = "vstudio"):
    if not os.path.exists(source_path):
        raise IOError("source_path does not exist so not skeleton can be built")
    '''
    for root, dirs, files in os.walk("."):
    path = root.split('/')
    print (len(path) - 1) *'---' , os.path.basename(root)       
    for file in files:
        print len(path)*'---', file
    '''

    """ Read .gitignore if existing. Fail if not existing.

    [to_ignore]
    with open(".gitignore") as fgit:
    for line in fgit:
        trimmed = line.strip()
        if trimmed and not trimmed.startswith("#"):
            to_ignore.append(trimmed)
    """

    """ return if it is ignored
    def is_ignored(path):
    for pattern in to_ignore:
        if fnmatch.fnmatch(path,pattern):
            return True
    return False
    """

    """ Recursive filtering
    for root, dirs, files in os.walk("."):
    dirs = [d for d in dirs if not is_ignored(d)]
    files = [f for f in files if not is_ignored(f)]
    print root, dirs, files
    """