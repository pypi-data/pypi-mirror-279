from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "OpenSCAD Python API"
LONG_DESCRIPTION = "A simple library to generate OpenSCAD code using Python."

setup(
    name="openscad-py",
    version=VERSION,
    author="Mickaël Fabrègue",
    author_email="<mickael.fabregue@proton.me>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=['openscad_py', 'openscad_py.*']),
    install_requires=[],  
    keywords=["python", "openscad", "3d", "2d", "cad", "modeling"],
    classifiers=[
        "Development Status :: 1 - Planning",
    ],
)
