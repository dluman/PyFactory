import setuptools

setuptools.setup(
    name="py-factory",
    version="0.1.0",
    packages=['py_factory'],
    package_dir={'py_factory': 'src'},
    include_package_data=True,
    description="A simple templating system for Python class files.",
    long_description="""
=======
PyFactory
=======

An simple templating system for Python class files which allows users to create, use, and expand on templates
bsaed on other Python files. There's an examplein the GitHub README documentation. Has no dependencies, and
no frills.

It's a work in progress.

Notes
=====
Requires a template file or pre-existing module to load information from. Can even copy system built-ins and
other modules on PATH.

Additional note: the module can't handle explicit inheritance yet. I need to fix that.
    """,
    long_description_content_type="text/x-rst",
    install_requires=[
      '',
    ],
    url="https://github.com/dluman/pyfactory"
 )
