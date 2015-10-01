.. ideskeleton documentation master file, created by
   sphinx-quickstart on Thu Oct 01 12:25:20 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ideskeleton's documentation
============================

This projects allows you to creat the needed files of some IDE's such as Visual Studio in order
to work with a Python project located in a plane folder structure.

Rationale
---------
It is common practice in Python open source projects not relying on any IDE. 
This tool allows you to have a clean folder structure that can be shared in GIT repositories
while being able to work with your favorite IDE in your workstation.

Basic usage
---------------
After getting the code you can exectue the package from the command line::

	python -m ideskeleton -f your-full-path

This will generate all needed files such as solution and project files for the Visual Studio case.

Off course, you can also import the package and customize the behavior as desired::

	from ideskeleton import builder
	builder.build("your_path", overwrite=True, ide="vstudio")

.. module:: ideskeleton

For normal use, all you have to do::

	import ideskeleton

This will import:

- The :func:`build` that allows to build the files needed for IDE

Using from the command line
---------------------------

In order to build the IDE files from command line you just type::

	python -m ideskeleton [-h] [-f] [-i {vstudio}] source_path

*positional arguments:*
  source_path           path of the folder structure used to generate the IDE
                        skeleton

*optional arguments:*
  -h, --help			show this help message and exit
  -f, --force			force overwrite existing solution and project files
  -i, --ide				choose IDE {vstudio}

builder module
--------------

.. automodule::builder

.. autofunction:: build()

ideprocesses module
-------------------

.. automodule:: ideskeleton.ideprocesses

.. autofunction:: ideskeleton.ideprocesses.vstudio_read

.. autofunction:: ideskeleton.ideprocesses.vstudio_write

Important notes
---------------
Just Visual Studio is supported so far, although adding new IDE's is pretty easy.

A number of opinionated conventions are enforced:

- .gitignore file is used to decide which files to consider
- Just ``*.py`` files are added with compile action.
- Any not ignored folder in the first level is added as a python project.
- Any not ignored folder in higher than first level are added as project folder.

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

