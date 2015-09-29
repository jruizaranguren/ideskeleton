
from os.path import abspath, basename, splitext, dirname, isabs, join
from uuid import uuid5, UUID

compilables = set([".py"])

ADD_CONTAINER = "container"
ADD_CONTENT = "content"
ADD_COMPILE = "compile"
ADD_FOLDER=  "folders"

def identifier(path):
    namespace = UUID("{D4A33062-9785-467D-8179-05177E00F1E2}")
    return uuid5(namespace,path)

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
        next_actions.append((ADD_CONTAINER,None,container))
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

def arrange_actions_into_structure(actions):
    structure = {}
    for action, container, path in actions:

        if action == ADD_CONTAINER:
            if not container:
                structure[path] = {
                    "content":[],
                    "projects":[]
                    }
            else:
                structure[container]["projects"].append(path)
                structure[path] = {
                    "identifier":identifier(path), 
                    "folders":[], 
                    "compile":[], 
                    "content":[]
                    }
        else:
            structure[container][action].append(path)
             

    return structure

def vstudio_write(actions, path):
    structure = arrange_actions_into_structure(actions)

    for file_name, metadata in structure.iteritems():
        name, extension = splitext(file_name)
        
        if extension == ".sln":
            full_path = join(path, file_name)
        else:
            full_path = join(path, name, file_name)

    # Write each file except IOException





processes = {
        "vstudio": [vstudio_read, None],
        None : [none_read, none_write]
    }
