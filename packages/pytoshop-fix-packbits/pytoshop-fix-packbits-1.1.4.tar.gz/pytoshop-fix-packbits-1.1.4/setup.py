#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "cython",
    "numpy>=1.11",
    "six",
    "typing",
    "packbits",
]

test_requirements = [
    'pytest'
]


extensions = []

setup(
    name='pytoshop-fix-packbits',
    version='1.1.4',
    description="A Python-based library to write Photoshop PSD files",
    author="original author: Michael Droettboom, modified by: radius5",
    author_email='info@radius5.co.jp',
    url='https://github.com/radius5-study/pytoshop-fix-packbits',
    packages=[
        'pytoshop',
        'pytoshop.user'
    ],
    package_dir={'pytoshop':
                 'pytoshop'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='pytoshop',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    ext_modules=extensions
)
