from setuptools import setup, find_packages

setup(
    name="finetool",
    version="0.0.0",
    description="",
    author="System Design Studio",
    author_email="silveryfu@gmail.com",
    license="Apache License, Version 2.0",
    packages=find_packages(exclude=("tests",)),
    python_requires='>=3.10',
    include_package_data=True,
    install_requires = open('requirements.txt').readlines(),
)

