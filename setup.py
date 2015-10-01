from setuptools import setup

setup(name='ideskeleton',
      version='0.10',
      description="Scaffolding of IDE project files such as Visual Studio from Python existing" \
          "folder structure",
      author="Javier Ruiz Aranguren",
      license="MIT",
      url="http://github.com/jruizaranguren/ideskeleton",
      packages=['ideskeleton', 'ideskeleton.builder', 'ideskeleton.ideprocesses']
      )

__author__ = "Javier Ruiz Aranguren"