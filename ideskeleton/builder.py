import os.path
from fnmatch import fnmatch
from .ideprocesses import processes

def read_gitignore(source_path):
    path = os.path.join(source_path,".gitignore")
    with open(path,'r') as fgit:
        valid_patterns = lambda l: l and not l.startswith("#")
        return list(filter(valid_patterns, map(str.strip, fgit)))

def is_ignored(item, patterns):
    return any([fnmatch(item, pattern) for pattern in patterns])

def traverse(source_path, process):
    patterns = read_gitignore(source_path)
    level = lambda path: path.count("\\") + path.count("/")
    base_level = level(source_path)
    actions = []
    for root,dirs,files in os.walk(source_path):
        remove_ignored(dirs, patterns, is_dir=True)
        remove_ignored(files, patterns)
        actions.extend(process(level(root) - base_level, root, dirs, files))
    return actions

def remove_ignored(alist, patterns, is_dir=False):
    checkdir = lambda x: x + "/" if is_dir else x
    to_ignore = [itm for itm in alist if is_ignored(checkdir(itm),patterns)]
    for toi in to_ignore:
        alist.remove(toi)

def build(source_path, overwrite = True, ide = None):
    if not os.path.exists(source_path):
        raise IOError("source_path does not exist so not skeleton can be built")

    read_process, write_process = processes[ide]
    actions = traverse(source_path, read_process)
    
    return write_process(actions, source_path, overwrite)

