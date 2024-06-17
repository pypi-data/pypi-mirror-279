#!/usr/bin/env python
import io
from os import path
from setuptools import setup

"""
:authors: Dmitry Batrov
:license: Apache License, Version 2.0
:copyright: (c) 2024, Dmitry Batrov
"""

def load_readme(fp):
    if path.exists(fp):
        with io.open(fp, encoding='utf8') as f:
            return f.read()
    return ""

def setup_package():
    root = path.abspath(path.dirname(__file__))
    readme_path = path.join(root, 'README.md')
    readme = load_readme(readme_path)

    setup(
        name='ru_parser_cv',
        version='1.0.1',
        author='Dmitry Batrov',
        author_email='d.batrov@yandex.ru',
        description=(
            u'Python module for parsing Russian CVs'
            u' and extracting information from them'
        ),
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/dmitry-batrov/ru_parser_cv',
        license='Apache License, Version 2.0',
        packages=['ru_parser_cv'],
        install_requires=['spacy >= 3.7.0', 'fuzzywuzzy', 'ru_cv_parse_model'],
        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
        ], 
        python_requires='>=3.6',
    )


if __name__ == '__main__':
    setup_package()
