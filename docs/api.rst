.. _api:

ideskeleton API Documentation
=============================

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