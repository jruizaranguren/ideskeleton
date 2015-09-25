import pytest
from ideskeleton import ideprocesses as ide

def test_none_read_it_just_returns_the_input_within_a_list():
    actual = ide.none_read(0,".",["dir1"],["file"])

    assert actual == [(0,".",["dir1"],["file"])]

def test_none_write_returns_input_ignoring_path():
    actual = ide.none_write([],"C:/projects")

    assert actual == []


'''
SKETCH IDEAS

# Once in a project, things are added iteratively 
    folders to ItemGroup Folders.
    python files to ItemGroup as  Compile
    rest of files to ItemGroup as Content
    + Guid of project, + Guid of type of project

# Once in a solution
    Solution files are added with no problem.


    add_solution
    add_project
    add_file_to_solution
    add_foder_to_project
    add_file_to_project (compile/content)

    Finally, overwrite:
    write sln
    write csprojs
    write log???

'''