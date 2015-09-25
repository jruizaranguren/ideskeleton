
def none_read(level, root, dirs, files):
    return [(level, root, dirs, files)]

def none_write(actions, path):
    return actions


processes = {
        "vstudio": [None, None],
        None : [none_read, none_write]
    }
