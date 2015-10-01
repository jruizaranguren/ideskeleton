from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ideskeleton',
      version='0.10',
      description="Scaffolding of IDE project files such as Visual Studio from Python existing" \
          "folder structure",
      long_description=readme(),
      author="Javier Ruiz Aranguren",
      license="MIT",
      url="http://github.com/jruizaranguren/ideskeleton",
      packages=['ideskeleton']
      )

__author__ = "Javier Ruiz Aranguren"