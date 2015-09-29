import pytest
from os.path import join
from ideskeleton import ideprocesses as ide

def test_none_read_it_just_returns_the_input_within_a_list():
    actual = ide.none_read(0,".",["dir1"],["file"])

    assert actual == [(0,".",["dir1"],["file"])]

def test_none_write_returns_input_ignoring_path():
    actual = ide.none_write([],"C:/projects")

    assert actual == []

def test_parse_path_at_first_level_returns_last_folder_name():
    container, relative = ide.parse_path(0, "C:/Projects/MySolution")

    assert (container, relative) == ("MySolution", "")

def test_parse_path_at_second_level_returns_last_folder_as_project_name():
    container, relative = ide.parse_path(1, "C:/Projects/MySolution/MyProject")

    assert (container, relative) == ("MyProject", "")

@pytest.mark.parametrize("level,path,expected", [
    (2, "C:/Projects/MySolution/MyProject/Folder1", ("MyProject", join("Folder1",""))),
    (2, "./MySolution/MyProject/Folder1", ("MyProject", join("Folder1",""))),
    (3, "./MySolution/MyProject/Folder1/Folder2", ("MyProject", join("Folder1","Folder2",""))),
    (4, "./MySolution/MyProject/Folder1/Folder2/Folder3", ("MyProject", join("Folder1","Folder2","Folder3","")))
])
def test_parse_path_at_higher_levels_returns_project_name_and_relative_path_to_it(level,path,expected):
    container, relative = ide.parse_path(level, path)
    assert (container, relative) == expected

def test_arrange_actions_into_structure_groups_actions_to_files_and_action_type():
    actions = [
        (ide.ADD_CONTAINER, None, "MySolution.sln"),
        (ide.ADD_CONTAINER, "MySolution.sln", "Proj1.pyproj"),
        (ide.ADD_CONTAINER, "MySolution.sln", "Proj2.pyproj"),
        (ide.ADD_COMPILE, "MySolution.sln","file1.py"),
        (ide.ADD_CONTENT, "MySolution.sln","file2.txt"),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir2","")),
        (ide.ADD_FOLDER, "Proj2.pyproj", join("sub_dir3","")),
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_CONTENT, "Proj1.pyproj", "sub_file2.txt"),
        (ide.ADD_CONTENT, "Proj2.pyproj", "sub_file3.txt")
        ]

    expected = {
        "MySolution.sln" : {
            ide.ADD_COMPILE : [
                "file1.py"
                ],
            ide.ADD_CONTENT : [
                "file2.txt"
                ],
            "projects" : [
                "Proj1.pyproj",
                "Proj2.pyproj"
                ]
            },
        "Proj1.pyproj" : {
            "identifier": ide.identifier("Proj1.pyproj"),
            ide.ADD_FOLDER: [
                join("sub_dir1",""),
                join("sub_dir2","")
                ],
            ide.ADD_COMPILE: [
                "sub_file1.py"
                ],
            ide.ADD_CONTENT: [
                "sub_file2.txt"
                ]
            },
        "Proj2.pyproj" : {
            "identifier": ide.identifier("Proj2.pyproj"),
            ide.ADD_FOLDER: [
                join("sub_dir3","")
                ],
            ide.ADD_COMPILE: [
                ],
            ide.ADD_CONTENT: [
                "sub_file3.txt"
                ]
            }
        }

    assert ide.arrange_actions_into_structure(actions) == expected

def test_vstudio_read_a_solution_is_created_at_level_zero_for_relative_paths():
    actual =  ide.vstudio_read(0,".", [],[])
    assert actual[0] == (ide.ADD_CONTAINER, None, "ideskeleton.sln")

def test_vstudio_read_a_solution_is_created_at_level_zero_for_absolute_paths():
    actual = ide.vstudio_read(0,"C:/Projects/MySolution",[],[])
    assert actual[0] == (ide.ADD_CONTAINER, None, "MySolution.sln")

def test_vstudio_read_files_at_the_first_level_are_added_as_solution_files():
    actual = ide.vstudio_read(0, "C:/Projects/MySolution", [], ["file1.py", "file2.txt"])
    expected = [
        (ide.ADD_CONTAINER, None, "MySolution.sln"),
        (ide.ADD_COMPILE, "MySolution.sln","file1.py"),
        (ide.ADD_CONTENT, "MySolution.sln","file2.txt")
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_the_first_level_are_added_as_solution_projects():
    actual = ide.vstudio_read(0, "C:/Projects/MySolution", ["dir1","dir2"], [])
    expected = [
        (ide.ADD_CONTAINER, None, "MySolution.sln"),
        (ide.ADD_CONTAINER, "MySolution.sln", "dir1.pyproj"),
        (ide.ADD_CONTAINER, "MySolution.sln", "dir2.pyproj")
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_the_second_level_are_added_as_project_folders_for_relative_path():
    actual = ide.vstudio_read(1, "./MySolution/Proj1", ["sub_dir1","sub_dir2"], [])
    expected = [
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir2",""))
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_the_second_level_are_added_as_project_folders_for_absolute_path():
    actual = ide.vstudio_read(1, "C:/Projects/MySolution/Proj1", ["sub_dir1","sub_dir2"], [])
    expected = [
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("sub_dir2",""))
        ]
    assert actual == expected

def test_vstudio_read_files_at_the_second_level_are_added_as_project_items_for_absolute_path():
    actual = ide.vstudio_read(1, "C:/Projects/MySolution/Proj1", [], ["sub_file1.py","sub_file2.py"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file2.py")
        ]
    assert actual == expected

def test_vstudio_read_files_at_the_second_level_are_added_as_project_items_for_relative_path():
    actual = ide.vstudio_read(1, "./MySolution/Proj1", [], ["sub_file1.py","sub_file2.py"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file2.py")
        ]
    assert actual == expected

def test_vstudio_read_files_at_the_second_level_distinguises_compilable_from_content_files():
    actual = ide.vstudio_read(1, "./MySolution/Proj1", [], ["sub_file1.py","sub_file2.txt"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", "sub_file1.py"),
        (ide.ADD_CONTENT, "Proj1.pyproj", "sub_file2.txt")
        ]
    assert actual == expected

def test_vstudio_read_files_at_a_higher_than_second_level_are_added_as_project_items_considering_relative_path_from_project_path():
    actual = ide.vstudio_read(2, "./MySolution/Proj1/Dir1", [], ["sub_file1.py","sub_file2.txt"])
    expected = [
        (ide.ADD_COMPILE, "Proj1.pyproj", join("Dir1","sub_file1.py")),
        (ide.ADD_CONTENT, "Proj1.pyproj", join("Dir1","sub_file2.txt"))
        ]
    assert actual == expected

def test_vstudio_read_dirs_at_a_higher_than_second_level_are_added_as_project_folders_considering_relative_path_from_project_path():
    actual = ide.vstudio_read(2, "C:/Projects/MySolution/Proj1/Dir1", ["sub_dir1","sub_dir2"], [])
    expected = [
        (ide.ADD_FOLDER, "Proj1.pyproj", join("Dir1","sub_dir1","")),
        (ide.ADD_FOLDER, "Proj1.pyproj", join("Dir1","sub_dir2",""))
        ]
    assert actual == expected


