from setuptools import setup, find_packages

setup(
    name="pystacho",
    version="0.1.4",
    author="Paul Marclay",
    author_email="paul.eduardo.marclay@gmail.com",
    description="A simple ORM for Python, inspired by ActiveRecord, of Rails framework.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/paul-ot/pystacho-orm",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'inflect',
        'pyyaml',
        'colorama',
    ],
)