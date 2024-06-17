# setup.py

from setuptools import setup, find_packages

setup(
    name='sankalp',
    version='0.4.8',
    packages=find_packages(),
    install_requires=[
        "curses",
        "webbrowser",
    ],
    entry_points={
        'console_scripts': [
            'sankalp = sankalp.cli:run_cli',
        ],
    },
    python_requires='>=3.6',
    author='Sankalp Shrivastava',
    author_email='s@sankalp.sh',
    description='A simple CLI package for Sankalp Shrivastava',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/1sankalp',
)
