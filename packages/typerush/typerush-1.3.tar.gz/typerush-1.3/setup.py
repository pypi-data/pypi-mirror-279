from setuptools import setup, find_packages

setup(
    name='typerush',
    version='1.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'curses-menu', 
    ],
    package_data={ '': ['*.json']},
    entry_points={
        'console_scripts': [
            'typerush = typing_1:main',  
        ],
    },
)
