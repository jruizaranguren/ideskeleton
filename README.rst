ideskeleton
===========

.. image:: https://travis-ci.org/jruizaranguren/ideskeleton.svg
    :target: https://travis-ci.org/jruizaranguren/ideskeleton

Scaffolding of IDE project files such as Visual Studio from Python existing folder structure.

Rationale
---------
It is common practice in Python open source projects not relying on any IDE. 
This tool allows you to have a clean folder structure that can be shared in GIT repositories
while being able to work with your favorite IDE in your workstation.

Install
-------

	``pip install ideskeleton`` 

Basic usage
-----------
You can execute the package from the command line::

	python -m ideskeleton -f your-full-path

This will generate all needed files such as solution and project files for the Visual Studio case.

Off course, you can also import the package and customize the behavior as desired::

	from ideskeleton import builder
	builder.build("your_path", overwrite=True, ide="vstudio")

For normal use, all you have to do::

	import ideskeleton

This will import:

- The **build** function that allows to build the files needed for IDE

Command line options
--------------------

In order to build the IDE files from command line you just type::

	python -m ideskeleton [-h] [-f] [-i {vstudio}] source_path

**positional arguments:**
  source_path:          path of the folder structure used to generate the IDE                         skeleton

**optional arguments:**
  -h, --help			show this help message and exit
  -f, --force			force overwrite existing solution and project files
  -i, --ide				choose IDE {vstudio}

API docs
--------------

Can find api documentation at readthedocs_.

.. _readthedocs: http://ideskeleton.readthedocs.org/en/latest/

Important notes
---------------
Just Visual Studio is supported so far, although adding new IDE's is pretty easy.

A number of opinionated conventions are enforced:

- .gitignore file is used to decide which files to consider
- Just ``*.py`` files are added with compile action.
- Any not ignored folder in the first level is added as a python project.
- Any not ignored folder in higher than first level are added as project folder.