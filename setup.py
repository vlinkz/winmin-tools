#!/usr/bin/python3
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='winmin',
    version='0.0.1',
    description='winmin core tools',
    author='Victor Fuentes',
    author_email='hyruleterminatirforce@gmail.com',
    python_requires='>=3.5, <4',
    project_urls={
        'Source': 'https://github.com/vlinkz',
    },
    packages=['winmin-scripts'],
    scripts=['winmin-scripts/winmin_install.py','winmin-scripts/winmin_yml_install.py','winmin-scripts/winmin_run.py'],
    entry_points = {
        'console_scripts': [
            'winmin-run = winmin_run:main',  
            'winmin-install = winmin_install:main',
            'winmin-yml-install = winmin_yml_install:main',                
        ],
    },
)
