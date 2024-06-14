from setuptools import setup, find_packages
import json


setup(
    name='typerusx',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'curses-menu', 
    ],
    package_data={
        '': ["sentences.json"],
    },
    entry_points={
        'console_scripts': [
            'typerusx = typing_1:main',  
        ],
    },
)



