try:
    import paver
except ImportError:
    # Ignore pavement during tests.
    pass
else:
    from paver.easy import *
    import paver.misctasks
    import paver.setuputils
    from paver.setuputils import setup

    from textwrap import dedent

    from setuptools import Extension, find_packages

    from schevodurus.release import VERSION


    setup(
        name='SchevoDurus',
        version=VERSION,
        description="Durus storage backend for Schevo",
        long_description=dedent("""
        SchevoDurus provides integration between the Durus_ object database
        for Python and the Schevo_ DBMS.

        You can also get the `latest development version
        <http://github.com/gldnspud/schevodurus/zipball/master#egg=SchevoDurus-dev>`__.

        SchevoDurus depends on Durus 3.9.
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
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Database :: Database Engines/Servers',
            'Topic :: Software Development :: Libraries :: '
                'Application Frameworks',
        ],
        keywords='database dbms',
        author='ElevenCraft Inc.',
        author_email='schevo@googlegroups.com',
        url='http://www.schevo.org/',
        license='MIT',
        packages=find_packages(exclude=['doc', 'tests']),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'xdserver >= 3.9',
        ],
#         dependency_links = [
#             'http://pypi.python.org/pypi/SchevoDurus',
#             'http://www.schevo.org/eggs/',
#         ],
        tests_require=[
            'nose >= 0.11.0',
            'schevo == dev, >= 3.1.0dev-20091002',
        ],
        test_suite='nose.collector',
        entry_points = """
        [schevo.backend]
        durus = schevodurus.backend:DurusBackend
        xdserver = schevodurus.backend:XdserverBackend
        """,
        )


    options(
        cog=Bunch(
            basdir='doc/source',
            includedir='doc/source',
            pattern='*.txt',
            beginspec='<==',
            endspec='==>',
            endoutput='<==end==>',
        ),
        sphinx=Bunch(
            docroot='doc',
            builddir='build',
            sourcedir='source',
        ),
    )


    @task
    @needs(['paver.doctools.cog', 'paver.doctools.html', 'paver.doctools.uncog'])
    def html():
        pass


    @task
    @needs('html')
    def docs():
        import webbrowser
        index_file = path('doc/build/html/index.html')
        webbrowser.open('file://' + index_file.abspath())


    @task
    def doctests():
        from paver.doctools import _get_paths
        import sphinx
        options.order('sphinx', add_rest=True)
        paths = _get_paths()
        sphinxopts = ['', '-b', 'doctest', '-d', paths.doctrees,
            paths.srcdir, paths.htmldir]
        ret = dry(
            "sphinx-build %s" % (" ".join(sphinxopts),), sphinx.main, sphinxopts)


    @task
    @needs(['doctests', 'nosetests'])
    def test():
        pass
