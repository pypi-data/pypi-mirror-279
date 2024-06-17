from setuptools import setup, find_packages

VERSION= '0.0.3'
DESCRIPTION = 'my first python package'
LONG_DESCRIPTION = 'my first python package - long description'

setup(
        name="firstmodulejeremylaitter",
        version=VERSION,
        author="jeremy laitter",
        author_email="jeremy.laitter@proton.me",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=['python', 'mytag'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ]
)

