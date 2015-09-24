import pytest
import ideskeleton as skeleton
import os

def test_if_source_path_does_not_exist_error(tmpdir):
    not_existing = os.path.join(tmpdir.dirname, "not_existing")
    with pytest.raises(IOError):
        skeleton.build(not_existing)

def test_if_gitignore_not_found_error(tmpdir):
    with pytest.raises(IOError):
        skeleton.build(tmpdir.dirname)

def test_read_gitignore_returns_valid_patterns(tmpdir):
    local = tmpdir.mkdir("test_read_gitignore").join(".gitignore")
    local.write_text(u".git/\n" +
                     "#this is a comment\n" + 
                     "\n" +
                     "*.sln\n" + 
                     "[Dd]ebug/\n", 'ascii')
    
    patterns = skeleton.builder.read_gitignore(local.dirname)
    
    assert patterns == [".git/", "*.sln", "[Dd]ebug/"]
    
 
if __name__ == "__main__":
    pytest.main()

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