import setuptools

setuptools.setup(
    name="springform",
    version="0.5.5",
    packages=['springform'],
    package_dir={'springform': 'src'},
    include_package_data=True,
    description="A simple templating system for Python class files.",
    long_description="""
==========
springform
==========

An simple templating system for Python class files which allows users to create, use, and expand on templates
bsaed on other Python files. There's an examplein the GitHub README documentation. Has no dependencies, and
no frills.

Always a work in progress.

Notes
=====
Requires a template file or pre-existing module to load information from. Can even copy system built-ins and
other modules on PATH. As of 0.2.0, inheritances are possible.
    """,
    long_description_content_type="text/x-rst",
    install_requires=[
      '',
    ],
    url="https://github.com/dluman/springform"
 )
