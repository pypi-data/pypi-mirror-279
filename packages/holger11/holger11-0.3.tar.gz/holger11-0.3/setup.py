from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='holger11',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
    ],
    author='Yaromir Gusev',
    author_email='yaromirarhideus@gmail.com',
    description='Example library for educational purposes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
