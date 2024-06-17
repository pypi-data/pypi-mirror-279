from setuptools import setup, find_packages

setup(
    name='HenModule',
    version='1.0',
    packages=find_packages(),
    install_requires=[
    ],
    author='carlos vassoler',
    author_email='carloshtvassoler@gmail.com',
    description='a python module to perform heat integration',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CarlosTadeuVassoler/hen-module',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
