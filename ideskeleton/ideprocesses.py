
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

    return next_actions


processes = {
        "vstudio": [vstudio_read, None],
        None : [none_read, none_write]
    }
