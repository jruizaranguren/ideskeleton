
def none_read(level, root, dirs, files):
    return [(level, root, dirs, files)]

def none_write(actions, path):
    print actions


processes = {
        "vstudio": [None, None],
        "none" : [none_read, none_write]
    }
