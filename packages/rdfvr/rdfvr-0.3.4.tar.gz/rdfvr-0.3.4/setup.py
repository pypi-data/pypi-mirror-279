from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="rdfvr",
    version="0.3.4",
    description="RDFVR: RDF Validation Report",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meng6/rdfvr",
    author="Meng Li",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas>=2.1.0", "pyshacl>=0.23.0", "rdflib>=6.3.2", "pyvis>=0.3.2", "networkx>=3.3"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
    entry_points='''
        [console_scripts]
        rdfvr=rdfvr:main
    ''',
)