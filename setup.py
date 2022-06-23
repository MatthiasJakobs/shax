#!/usr/bin/env python

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
        name='shax',
        packages=['shax'],
        version='0.1',
        description='Extensible Shapley value calculator',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Matthias Jakobs, Sascha Muecke',
        author_email='matthias.jakobs@tu-dortmund.de',
        url='https://github.com/MatthiasJakobs/shax',
        requires=['numpy']
)
