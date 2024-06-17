from setuptools import setup, find_packages

requires = [
    'stats_arrays>=0.6.4',
    'synonym_dict>=0.1.1',
    'numpy<2.0'
]

'''
VERSION HISTORY
0.1.1 - 16 June 2024 - improve requirements specification

0.1.0 - 18 November 2020 - Initial setup 
'''

VERSION = '0.1.1'

setup(
    name="unit_gears",
    version=VERSION,
    author="Brandon Kuczenski",
    author_email="bkuczenski@ucsb.edu",
    license=open('LICENSE').read(),
    install_requires=requires,
    url="https://github.com/bkuczenski/unit_gears",
    summary="A library of uncertain models for the industrial operation of fishing gears",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages()
)
