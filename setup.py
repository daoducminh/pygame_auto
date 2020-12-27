# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='pygame_auto',
    version='1.0',
    author='minhdao',
    description='Pygame Self Driving',
    packages=find_packages(exclude=[
        'docs',
        'tests',
        'static',
        'templates',
        '.gitignore',
        'README.md',
        'images',
        '.vscode',
    ]),
    install_requires=[
        'pylint',
        'autopep8',
        'rope',
        'python-dotenv',
        'pygame',
        'pygame_gui',
        'pymunk',
        'networkx',
        'matplotlib',
        'pandas',
        'sympy'
    ]
)
