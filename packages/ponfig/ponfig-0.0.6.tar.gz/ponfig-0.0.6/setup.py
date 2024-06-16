# setup.py

from setuptools import setup, find_packages

setup(
    name='ponfig',
    version='0.0.6',
    packages=find_packages(),
    description='A simple configuration and environment management package.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='zeturn',
    author_email='hollowdata@outlook.com',
    url='https://hollowdata.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
