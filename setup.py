__version__ = '3.1a3'

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

    You can also get the `latest development version
    <http://github.com/gldnspud/schevodurus/zipball/master#egg=SchevoDurus-dev>`__.

    SchevoDurus depends on Durus 3.8.
    We maintain a `copy of Durus on github <http://github.com/gldnspud/durus/>`__
    and for your convenience provide a
    `Windows Python 2.5 egg
    <http://www.schevo.org/eggs/Durus-3.8-py2.5-win32.egg>`__
    and a
    `Mac OS X 10.5 Python 2.5 i386 egg
    <http://www.schevo.org/eggs/Durus-3.8-py2.5-macosx-10.5-i386.egg>`__.

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

    url='http://www.schevo.org/wiki/SchevoDurus',

    license='LGPL',

    platforms=['UNIX', 'Windows'],

    packages=find_packages(exclude=['doc', 'tests']),

    include_package_data=True,

    zip_safe=False,

    install_requires=[
    'Durus == 3.8',
    ],

    tests_require=[
    'nose >= 0.10.4',
    ],
    test_suite='nose.collector',

    extras_require={
    },

    dependency_links = [
    'http://pypi.python.org/pypi/SchevoDurus',
    'http://www.schevo.org/eggs/',
    ],

    entry_points = """
    [schevo.backend]
    durus = schevodurus.backend:DurusBackend
    """,
    )
