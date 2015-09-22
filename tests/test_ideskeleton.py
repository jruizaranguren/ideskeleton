'''
SKETCH IDEAS

def build(source_path="./", overwrite=True):
    # Path must exist
    # Files must be writtable (if they are created and opened exception)
   
    ignore = parse_gitignore_if_exists(source_path)

    sln_file = create_sln(source_path) # Last tag after / is the solution name
    proj_files = [create_proj(path) for path in get_dir(source_path)]
    # Path must have some projectable sources.
    sln_file.add(proj_files)
    sln_file_add(non_excluded_files_as_solution_files)

    def traverse(path,container = None, level = 0):
        if excluded(path):
            return

        if path is folder and not container:
            sln = create_sln(path)
            for child in path:
                traverse(child, sln, level)

        if path is folder and is_solution(container):
            proj = create_proj(path)
            for child in path:
                traverse(child, proj, level += 1)
       
        if path is folder and is_project(container):
            container.add(path)
            for child in path:
                traverse(child, proj, level + = 1)

        if path is file:
            container.add(path)

    Finally:
    write sln
    write csprojs
    write log???

    have a main to be used as application with simple args (source_path, overwrite).
    
'''