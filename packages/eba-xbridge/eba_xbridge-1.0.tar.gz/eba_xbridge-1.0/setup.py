"""
Setup.py for DRR package
"""

import os

import setuptools

setupPath = os.path.abspath(os.path.dirname(__file__))

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open('xbridge/__version__.py', 'r') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about['project'],
    version=about['version'],
    author=about['author'],
    author_email=about['author_email'],
    description=about['description'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=about['url'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['.env', '*.env'],
        'Testing': ['*']
    },
    license='Apache 2.0',
    license_files='LICENSE',
    project_urls={
        'Bug Tracker': 'https://github.com/Meaningful-Data/xbridge/issues',
        'Documentation': 'https://docs.xbridge.meaningfuldata.eu',
        'Source Code': 'https://github.com/Meaningful-Data/xbridge'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "pandas==2.2.2",
        "lxml==5.2.2",
        "py7zr==0.21.0"
    ],
)
