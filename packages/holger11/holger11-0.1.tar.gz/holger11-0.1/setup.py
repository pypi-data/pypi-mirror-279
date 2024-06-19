from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name='holger11',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
    ],  # Add a comma here
    author='Yaromir Gusev',
    author_email='yaromirarhideus@gmail.com',
    description='asdasdasda',

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT'
)
