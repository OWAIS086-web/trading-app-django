import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
name='django-admin-volt',
version='1.0.10',
zip_safe=False,
packages=find_packages(),
include_package_data=True,
description='Modern template for Django admin interface',
long_description=README,
long_description_content_type="text/markdown",
url='https://appseed.us/product/volt-dashboard/django/',
author='AppSeed.us',
author_email='support@appseed.us',
license='MIT License',
classifiers=[
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Environment :: Web Environment',
    'Topic :: Software Development',
    'Topic :: Software Development :: User Interfaces',
    ],
)


from setuptools import setup, find_packages

version = '5.2.0'

setup(
    name='django-bower',
    version=version,
    description="Integrate django with bower",
    long_description=open('README.rst').read(),
    classifiers=[
        'Framework :: Django',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    author='Vladimir Iakovlev',
    author_email='nvbn.rm@gmail.com',
    url='https://github.com/nvbn/django-bower',
    license='BSD',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'django',
        'six',
    ],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
