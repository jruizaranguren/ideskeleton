
from os.path import abspath, basename

def none_read(level, root, dirs, files):
    return [(level, root, dirs, files)]

def none_write(actions, path):
    return actions

def vstudio_read(level, root, dirs, files):
    next_actions = []
    solution_name = basename(abspath(root))
    next_actions.append(("add_solution",solution_name))
    return next_actions


processes = {
        "vstudio": [vstudio_read, None],
        None : [none_read, none_write]
    }
