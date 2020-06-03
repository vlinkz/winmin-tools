from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='winmin',  # Required
    version='0.0.1',  # Required
    description='winmin core tools',  # Optional
    author='Victor Fuentes',  # Optional
    author_email='hyruleterminatirforce@gmail.com',  # Optional
    #packages=find_packages(where='pywinminsetup'),  # Required
    python_requires='>=3.5, <4',
    project_urls={  # Optional
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
