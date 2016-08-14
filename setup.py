#!/usr/bin/env python3

from setuptools import setup
from src.django_customizable_ace import __version__ as current_version
    

setup(
    name='django_customizable_ace',
    version=current_version,
    description='Allow to easily use Ace editor in your django projects',
    license='4-clause "BSD License"',
    author='Pirheas',
    url='https://github.com/Pirheas/django-customizable-ace',
    packages=['django_customizable_ace'],
    package_dir={'': 'src'},
    install_requires=['django'],
    include_package_data=True,
    package_data={'': ['src/django_customizable_ace/static/django_customizable_ace/js/*.js',
                       'src/django_customizable_ace/static/django_customizable_ace/css/*.css',
                       'src/django_customizable_ace/static/django_customizable_ace/ace/*.js',
                       'include src/django_customizable_ace/static/django_customizable_ace/ace/*.css',
                       'src/django_customizable_ace/templates/*.html']}
)

