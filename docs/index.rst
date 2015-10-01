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

Usage
-----
After getting the code you can exectue the package from the command line::

	python -m ideskeleton -f your-full-path

This will generate all needed files such as solution and project files for the Visual Studio case.

Off course, you can also import the package and customize the behavior as desired::

	from ideskeleton import builder
	builder.build("your_path", overwrite=True, ide="vstudio")

For more information about how to use this library, see the :ref:`api`.

Important notes
---------------
Just Visual Studio is supported so far, although adding new IDE's is pretty easy.

A number of opinionated conventions are enforced:

- .gitignore file is used to decide which files to consider
- Just *.py files are added with compile action.
- Any not ignored folder in the first level is added as a python project.
- Any not ignored folder in higher than first level are added as project folder.

Contents
========

.. toctree::
   :maxdepth: 2

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

