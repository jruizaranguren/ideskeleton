import os.path

def read_gitignore(source_path):
    path = os.path.join(source_path,".gitignore")
    with open(path,'r') as fgit:
        valid_patterns = lambda l: l and not l.startswith("#")
        return filter(valid_patterns, map(str.strip, fgit))

def build(source_path, overwrite = True, ide = "vstudio"):
    if not os.path.exists(source_path):
        raise IOError("source_path does not exist so not skeleton can be built")

    patterns = read_gitignore(source_path)

    # test writabble .sln and .csproj files.

    """ Recursive filtering
     for root,dirs,files in os.walk("."):
   ....:     igdirs = [d for d in dirs if is_ignored(d+'\\')]
   ....:     igfiles = [f for f in files if is_ignored(f)]
   ....:     for d in igdirs:
   ....:         dirs.remove(d)
   ....:     for f in igfiles:
   ....:         files.remove(f)
   ....:     print root,  dirs, files    
   """