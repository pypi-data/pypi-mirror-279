from setuptools import setup, find_packages

setup(
    name='sankalp',
    version='0.1.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sankalp = sankalp:run',
        ],
    },
    install_requires=[],
    description="A simple interactive CLI for Sankalp Shrivastava",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/1Sankalp',  # Update this with the actual URL
    author='Sankalp Shrivastava',
    author_email='s@sankalp.sh',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
