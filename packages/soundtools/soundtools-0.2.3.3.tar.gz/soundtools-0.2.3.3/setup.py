from setuptools import setup, find_packages
setup(
name='soundtools',
version='0.2.3.3',
description="used to work with sounds waves",
long_description="""made by Mohammad Erfan Karami
github: https://github.com/erfan-ops

version: 0.2.3.3

this package is used to create, play and save sound files
it has some basic sound waves although you can add your own and modify the package.

it stores the sound waves as numpy arrays and uses pyaudio for playback
and uses matplotlib to visualize the waves""",
author='Mohammad Erfan Karami',
author_email='erfan012amir016@gmail.com',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)