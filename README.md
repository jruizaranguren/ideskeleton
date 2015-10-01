# ideskeleton

[![Build Status](https://travis-ci.org/jruizaranguren/ideskeleton.svg?branch=master)](https://travis-ci.org/jruizaranguren/ideskeleton)

Scaffolding of IDE project files such as Visual Studio from Python existing folder structure

## Rationale

It is common practice in Python open source projects not relying on any IDE. 
This tool allows you to have a clean folder structure that can be shared in GIT repositories
while being able to work with your favorite IDE in your workstation.

## Usage 

After getting the code you can exectue the package from the command line::
```
    python -m ideskeleton -f your-full-path
```

This will generate all needed files such as solution and project files for the Visual Studio case.

Off course, you can also import the package and customize the behavior as desired:

```
	from ideskeleton import builder
	builder.build("your_path", overwrite=True, ide="vstudio")
```

For more information about how to use this library, see [the docs.](http://ideskeleton.readthedocs.org/en/latest/)

Important notes
---------------
Just Visual Studio is supported so far, although adding new IDE's is pretty easy.

A number of opinionated conventions are enforced:

- .gitignore file is used to decide which files to consider
- Just ``*.py`` files are added with compile action.
- Any not ignored folder in the first level is added as a python project.
- Any not ignored folder in higher than first level are added as project folder.
