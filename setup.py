__version__ = '3.1a2'

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
    <http://getschevo.org/hg/repos.cgi/schevodurus-dev/archive/tip.tar.gz#egg=SchevoDurus-dev>`__.

    At the moment, it depends on a `friendly fork of Durus 3.7
    <http://getschevo.org/hg/repos.cgi/durusfork-dev/archive/3.7-schevo2.tar.gz#egg=Durus-3.7-schevo2>`__
    (`Windows Python 2.5 egg
    <http://getschevo.org/eggs/Durus-3.7_schevo2-py2.5-win32.egg>`__ and
    `latest development version
    <http://getschevo.org/hg/repos.cgi/durusfork-dev/archive/tip.tar.gz#egg=Durus-dev>`__
    also available).

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
    'Durus == 3.8',
    ],

    tests_require=[
    'nose >= 0.10.1',
    ],
    test_suite='nose.collector',

    extras_require={
    },

    dependency_links = [
    'http://pypi.python.org/pypi/SchevoDurus',
    'http://getschevo.org/eggs/',
    ],

    entry_points = """
    [schevo.backend]
    durus = schevodurus.backend:DurusBackend
    """,
    )
