from setuptools import setup, find_packages
from os import path

# Get the long description from the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='javier_vidal',
    version='0.2.1',
    description='Javier vidal',
    author='Javier vidal',
    author_email='abascur2024@udec.cl',
    packages=find_packages(), 
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)