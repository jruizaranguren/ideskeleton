import pytest
import ideskeleton as skeleton
from ideskeleton import builder
import os
import types

def test_build_can_be_called_from_skeleton_package():
    assert type(skeleton.build) == types.FunctionType

def test_build_if_source_path_does_not_exist_error(tmpdir):
    not_existing = os.path.join(tmpdir.dirname, "not_existing")
    with pytest.raises(IOError):
        builder.build(not_existing)

def test_build_if_gitignore_not_found_error(tmpdir):
    with pytest.raises(IOError):
        builder.build(tmpdir.dirname)

def test_read_gitignore_returns_valid_patterns(tmpdir):
    local = tmpdir.mkdir("test_read_gitignore").join(".gitignore")
    local.write_text(u".git/\n" +
                     "#this is a comment\n" + 
                     "\n" +
                     "*.sln\n" + 
                     "[Dd]ebug/\n", 'ascii')
    
    patterns = builder.read_gitignore(local.dirname)
    
    assert patterns == [".git/", "*.sln", "[Dd]ebug/"]

@pytest.mark.parametrize("input,expected", [
    (".git/", True),
    ("sln", False),
    ("debug/", True),
    ("myname.sln", True),
    ("C:\path\myname.sln", True)
])
def test_is_ignored_check_if_patterns_are_satisfied(input, expected):
    patterns = [".git/", "*.sln", "[Dd]ebug/"]

    assert builder.is_ignored(input, patterns) == expected

def test_remove_ignored_modify_input_list_of_files_in_place():
    patterns = [".git/", "*.sln", "[Dd]ebug/"]
    files = [".git", "C:\path\myname.sln", "code.py"]

    builder.remove_ignored(files, patterns)

    assert files == [".git", "code.py"]

def test_remove_ignored_modify_input_list_of_dirs_in_place():
    patterns = [".git/", "*.sln", "[Dd]ebug/"]

    dirs = [".git", "ideskeleton","debug"]
    builder.remove_ignored(dirs, patterns, True)

    assert dirs == ["ideskeleton"]
 
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


'''