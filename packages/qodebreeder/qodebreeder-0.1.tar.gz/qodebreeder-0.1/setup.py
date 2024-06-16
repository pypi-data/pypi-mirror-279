"""
Setup script for qodebreeder Python package.

This script uses setuptools to package and distribute qodebreeder.
"""

from setuptools import setup, find_packages

setup(
    name='qodebreeder',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Frandy Slueue',
    author_email='frandy4ever@gmail.com',
    description='A Python package for random element selection from various data structures.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Qode-Breeder/qodebreeder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
