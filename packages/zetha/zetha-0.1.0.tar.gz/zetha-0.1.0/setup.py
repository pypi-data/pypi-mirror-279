from setuptools import setup, find_packages # type: ignore

setup(
    name='zetha',
    version='0.1.0',
    author='Bruno Moretti',
    url='https://github.com/StafSis/Zetha',
    packages=find_packages(where='zetha'),
    package_dir={'': 'zetha'},
)
