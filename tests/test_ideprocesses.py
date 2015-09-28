import pytest
import os.path
from ideskeleton import ideprocesses as ide

def test_none_read_it_just_returns_the_input_within_a_list():
    actual = ide.none_read(0,".",["dir1"],["file"])

    assert actual == [(0,".",["dir1"],["file"])]

def test_none_write_returns_input_ignoring_path():
    actual = ide.none_write([],"C:/projects")

    assert actual == []

def test_vstudio_a_solution_is_created_at_level_zero_for_relative_paths():
    actual =  ide.vstudio_read(0,".", [],[])
    assert actual[0] == ("add_solution", None, "ideskeleton")

def test_vstudio_a_solution_is_created_at_level_zero_for_absolute_paths():
    actual = ide.vstudio_read(0,"C:/Projects/MySolution",[],[])
    assert actual[0] == ("add_solution", None, "MySolution")

def test_vstudio_files_at_the_first_level_are_added_as_solution_files():
    actual = ide.vstudio_read(0, "C:/Projects/MySolution", [], ["file1", "file2"])
    expected = [
        ("add_solution", None, "MySolution"),
        ("add_file_to_solution", "MySolution","file1"),
        ("add_file_to_solution", "MySolution","file2")
        ]
    assert actual == expected

def test_vstudio_dirs_at_the_first_level_are_added_as_solution_projects():
    actual = ide.vstudio_read(0, "C:/Projects/MySolution", ["dir1","dir2"], [])
    expected = [
        ("add_solution", None, "MySolution"),
        ("add_project_to_solution", "MySolution", "dir1"),
        ("add_project_to_solution", "MySolution", "dir2")
        ]
    assert actual == expected

def test_vstudio_dirs_at_the_second_level_are_added_as_project_folders_for_relative_path():
    actual = ide.vstudio_read(1, "./MySolution/Dir1", ["sub_dir1","sub_dir2"], [])
    expected = [
        ("add_folder_to_project", "Dir1", "sub_dir1"),
        ("add_folder_to_project", "Dir1", "sub_dir2")
        ]
    assert actual == expected

def test_vstudio_dirs_at_the_second_level_are_added_as_project_folders_for_absolute_path():
    actual = ide.vstudio_read(1, "C:/Projects/MySolution/Dir1", ["sub_dir1","sub_dir2"], [])
    expected = [
        ("add_folder_to_project", "Dir1", "sub_dir1"),
        ("add_folder_to_project", "Dir1", "sub_dir2")
        ]
    assert actual == expected

def test_vstudio_files_at_the_second_level_are_added_as_project_items_for_absolute_path():
    actual = ide.vstudio_read(1, "C:/Projects/MySolution/Dir1", [], ["sub_file1","sub_file2"])
    expected = [
        ("add_file_to_project", "Dir1", "sub_file1"),
        ("add_file_to_project", "Dir1", "sub_file2")
        ]
    assert actual == expected

def test_vstudio_files_at_the_second_level_are_added_as_project_items_for_relative_path():
    actual = ide.vstudio_read(1, "./MySolution/Dir1", [], ["sub_file1","sub_file2"])
    expected = [
        ("add_file_to_project", "Dir1", "sub_file1"),
        ("add_file_to_project", "Dir1", "sub_file2")
        ]
    assert actual == expected

#def test_vstudio_files_at_a_higher_than_second_level_are_added_as_project_items_considering_relative_path_from_project_path():
#    pass

#def test_vstudio_dirs_at_a_higher_than_second_level_are_added_as_project_folders_considering_relative_path_from_project_path():
#    pass




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