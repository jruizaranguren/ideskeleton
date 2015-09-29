
from os.path import abspath, basename, splitext, dirname, isabs, join

compilables = set([".py"])

def parse_path(level, path):
    if level > 1:
        proj, rel_path = parse_path(level - 1, dirname(path))
        return proj, join(rel_path, basename(path), "")
    else:
        return basename(path), ""

def none_read(level, root, dirs, files):
    return [(level, root, dirs, files)]

def none_write(actions, path):
    return actions

def vstudio_read(level, root, dirs, files):
    next_actions = []

    container, relative_path = parse_path(level, abspath(root))

    if level == 0:
        next_actions.append(("add_solution",None,container))
        for file in files:
            next_actions.append(("add_file_to_solution",container, file))
        for dir in dirs:
            next_actions.append(("add_project_to_solution", container, dir))

    if level >= 1:
        for dir in dirs:
            next_actions.append(("add_folder_to_project",container,join(relative_path,dir,"")))
        for file in files:
            name, extension = splitext(file)
            if extension in compilables: 
                next_actions.append(("compile_to_project",container,join(relative_path,file)))
            else:
                next_actions.append(("content_to_project",container,join(relative_path,file)))

    return next_actions


processes = {
        "vstudio": [vstudio_read, None],
        None : [none_read, none_write]
    }
