from setuptools import setup, find_packages

_locals = {}
with open("ctdk/version.py") as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

setup(
    name='ctdk',
    version=version,
    description='A development toolkit for Codetech.',
    author='jimin',
    author_email='jimin@codetech.top',
    url='https://www.python.org/',
    license='GPL-3.0-or-later',
    keywords=['codetech', 'ctlib', 'ctdk', 'ctlib-devkit'],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        "PyYAML>=5.4",
        "pydantic>=2.0",
    ],
    include_package_data=True,
)
