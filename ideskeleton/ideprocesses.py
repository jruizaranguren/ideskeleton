
from os.path import abspath, basename, splitext, dirname, isabs, join
from uuid import uuid5, UUID

compilables = set([".py"])

ADD_CONTAINER = "container"
ADD_CONTENT = "content"
ADD_COMPILE = "compile"
ADD_FOLDER=  "folders"

PROJ_TYPE = "888888A0-9F3D-457C-B088-3A5042F75D52"
SOL_TYPE = "2150E333-8FDC-42A3-9474-1A3956D46DE8"

def identifier(path):
    namespace = UUID("{D4A33062-9785-467D-8179-05177E00F1E2}")
    return uuid5(namespace,path)

def parse_path(level, path):
    if level > 1:
        proj, rel_path = parse_path(level - 1, dirname(path))
        return proj, join(rel_path, basename(path), "")
    else:
        return basename(path), ""

def none_read(level, root, dirs, files):
    return [(level, root, dirs, files)]

def none_write(actions, path, overwrite = False):
    return actions

def vstudio_read(level, root, dirs, files):
    next_actions = []

    container, relative_path = parse_path(level, abspath(root))

    if level == 0:
        container += ".sln"
        next_actions.append((ADD_CONTAINER,None,container))
        for dir in dirs:
            next_actions.append((ADD_CONTAINER, container, dir + ".pyproj"))

    if level >= 1:
        container += ".pyproj"
        for dir in dirs:
            next_actions.append((ADD_FOLDER,container,join(relative_path,dir,"")))

    for file in files:
        name, extension = splitext(file)
        if extension in compilables: 
            next_actions.append((ADD_COMPILE,container,join(relative_path,file)))
        else:
            next_actions.append((ADD_CONTENT,container,join(relative_path,file)))

    return next_actions

def arrange_actions_into_structure(actions):
    structure = {}
    for action, container, path in actions:

        if action == ADD_CONTAINER:
            if not container:
                structure[path] = {
                    "identifier":identifier(path),
                    "compile":[],
                    "content":[],
                    "projects":[]
                    }
            else:
                structure[container]["projects"].append(path)
                structure[path] = {
                    "identifier":identifier(path), 
                    "folders":[], 
                    "compile":[], 
                    "content":[]
                    }
        else:
            structure[container][action].append(path)

    return structure

def vstudio_write(actions, path, overwrite = False):
    structure = arrange_actions_into_structure(actions)

    for file_name, metadata in structure.iteritems():
        name, extension = splitext(file_name)
        lines = []
        
        if extension == ".sln":
            full_path = join(path, file_name)
            lines.extend([
                "",
                "Microsoft Visual Studio Solution File, Format Version 12.00",
                "# Visual Studio 14",
                "VisualStudioVersion = 14.0.23107.0",
                "MinimumVisualStudioVersion = 10.0.40219.1"
                ])
        
            for project in metadata["projects"]:
                proj_name = splitext(project)[0]
                lines.append("Project(\"{{{}}}\") = \"{}\", \"{}\", \"{{{}}}\"".format(
                    PROJ_TYPE,
                    name, 
                    join(proj_name,project),
                    str(structure[project]["identifier"])))
                lines.append("EndProject")
             
            all_content = metadata[ADD_CONTENT].extend(metadata[ADD_COMPILE])

            if all_content:
                lines.extend([
                    "Project(\"{{{}}}\") = \"Solution Items\", \"Solution Items\", \"{{}}\"".format(SOL_TYPE, str(metadata["identifier"])),
                    "\tProjectSection(SolutionItems) = preProject",
                    ])

                for item in all_content:
                    lines.append(["{} = {}".format(item,item)])

                lines.extend([
                    "\tEndProjectSection",
                    "EndProject"
                    ])

            lines.extend([
                "Global",
                "\tGlobalSection(SolutionConfigurationPlatforms) = preSolution",
                "\t\tDebug|Any CPU = Debug|Any CPU",
                "\t\tRelease|Any CPU = Release|Any CPU",
                "\tEndGlobalSection"
                ])

            if metadata["projects"]:
                lines.append("\tGlobalSection(ProjectConfigurationPlatforms) = postSolution")
                for project in metadata["projects"]:
                    identifier = str(structure[project]["identifier"])
                    lines.append("\t\t{{{}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU".format(identifier))
                    lines.append("\t\t{{{}}}.Release|Any CPU.ActiveCfg = Release|Any CPU".format(identifier))
                lines.append("\tEndGlobalSection")

            lines.extend([
                "\tGlobalSection(SolutionProperties) = preSolution",
                "\t\tHideSolutionNode = FALSE",
                "\tEndGlobalSection",
                "EndGlobal"
                ])

        else:
            full_path = join(path, name, file_name)
            identifier = str(metadata["identifier"])
            
            lines.extend([
                "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
                "<Project ToolsVersion=\"4.0\" xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\" DefaultTargets=\"Build\">",
                "\t<PropertyGroup>",
                "\t\t<Configuration Condition=\" '$(Configuration)' == '' \">Debug</Configuration>",
                "\t\t<SchemaVersion>2.0</SchemaVersion>",
                "\t\t<ProjectGuid>{{{}}}</ProjectGuid>".format(identifier),
                "\t\t<ProjectHome />",
                "\t\t<StartupFile />",
                "\t\t<SearchPath />",
                "\t\t<WorkingDirectory>../{}</WorkingDirectory>".format(name),
                "\t\t<OutputPath>.</OutputPath>",
                "\t\t<ProjectTypeGuids>{{{}}}</ProjectTypeGuids>".format(PROJ_TYPE),
                "\t\t<LaunchProvider>Standard Python launcher</LaunchProvider>",
                "\t\t<InterpreterId />",
                "\t\t<InterpreterVersion />",
                "\t</PropertyGroup>",
                "\t<PropertyGroup Condition=\"'$(Configuration)' == 'Debug'\" />",
                "\t<PropertyGroup Condition=\"'$(Configuration)' == 'Release'\" />",
                "\t<PropertyGroup>",
                "\t\t<VisualStudioVersion Condition=\" '$(VisualStudioVersion)' == '' \">10.0</VisualStudioVersion>",
                "\t\t<PtvsTargetsFile>$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\\v$(VisualStudioVersion)\Python Tools\Microsoft.PythonTools.targets</PtvsTargetsFile>",
                "\t</PropertyGroup>"
                ])

            if metadata[ADD_COMPILE]:
                lines.append("\t<ItemGroup>")
                for item in metadata[ADD_COMPILE]:
                    lines.append("\t\t<Compile Include=\"../{}/{}\" />".format(name, item))
                lines.append("\t</ItemGroup>")

            if metadata[ADD_FOLDER]:
                lines.append("\t<ItemGroup>")
                for item in metadata[ADD_FOLDER]:
                    lines.append("\t\t<Folder Include=\"{}\" />".format(item))
                lines.append("\t</ItemGroup>")

            if metadata[ADD_CONTENT]:
                lines.append("\t<ItemGroup>")
                for item in metadata[ADD_COMPILE]:
                    lines.append("\t\t<Content Include=\"{}\" />".format(item))
                lines.append("\t</ItemGroup>")

            lines.extend([
                "\t<Import Project=\"$(PtvsTargetsFile)\" Condition=\"Exists($(PtvsTargetsFile))\" />",
                "\t<Import Project=\"$(MSBuildToolsPath)\Microsoft.Common.targets\" Condition=\"!Exists($(PtvsTargetsFile))\" />",
                "</Project>"
                ])

        mode = "w+" if overwrite else "w"

        with open(full_path, mode) as file:
            file.write("\n".join(lines))

processes = {
        "vstudio": [vstudio_read, vstudio_write],
        None : [none_read, none_write]
    }
