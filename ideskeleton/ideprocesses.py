
from os.path import abspath, basename

def none_read(level, root, dirs, files):
    return [(level, root, dirs, files)]

def none_write(actions, path):
    return actions

def vstudio_read(level, root, dirs, files):
    next_actions = []

    if level == 0:
        solution_name = basename(abspath(root))
        next_actions.append(("add_solution",None,solution_name))
        for file in files:
            next_actions.append(("add_file_to_solution",solution_name, file))
        for dir in dirs:
            next_actions.append(("add_project_to_solution", solution_name, dir))

    if level == 1:
        project_name = basename(abspath(root))
        for dir in dirs:
            # WARN: This is not correct. Split in add_content_to_project and add_compile_to_project
            next_actions.append(("add_folder_to_project",project_name,dir))
        for file in files:
            next_actions.append(("add_file_to_project",project_name,file))

    if level > 1:
        root_path = abspath(root)
        # Need a function to extract project name an relative path to current level items
        pass

    return next_actions


processes = {
        "vstudio": [vstudio_read, None],
        None : [none_read, none_write]
    }
