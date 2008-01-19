__version__ = '3.1a1'

from setuptools import setup, Extension, find_packages
import sys, os
import textwrap


setup(
    name="SchevoDurus",

    version=__version__,

    description="Durus storage backend for Schevo",

    long_description=textwrap.dedent("""
    SchevoDurus provides integration between the Durus_ object database
    for Python and the Schevo_ DBMS.

    The latest development version is available in a `Subversion
    repository <http://schevo.org/svn/trunk/Durus#egg=SchevoDurus-dev>`__.

    .. _Schevo: http://schevo.org/

    .. _Durus: http://www.mems-exchange.org/software/durus/
    """),

    classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Database :: Database Engines/Servers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    keywords='database dbms',

    author='Orbtech, L.L.C. and contributors',
    author_email='schevo@googlegroups.com',

    url='http://schevo.org/wiki/SchevoDurus',

    license='LGPL',

    platforms=['UNIX', 'Windows'],

    packages=find_packages(exclude=['doc', 'tests']),

    include_package_data=True,

    zip_safe=False,

    install_requires=[
    'Durus == 3.7-schevo2',
    ],

    tests_require=[
    'nose >= 0.10.1',
    ],
    test_suite='nose.collector',

    extras_require={
    },

    dependency_links = [
    ],

    entry_points = """
    [schevo.backend]
    durus = schevodurus.backend:DurusBackend
    """,
    )
