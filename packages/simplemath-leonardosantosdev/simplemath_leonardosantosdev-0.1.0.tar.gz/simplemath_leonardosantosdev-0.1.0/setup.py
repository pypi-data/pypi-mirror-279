# setup.py

from setuptools import setup, find_packages

setup(
    name='simplemath_leonardosantosdev',
    version='0.1.0',
    author='Leonardo Santos',
    author_email='leodossantosldsl@gmail.com',
    description='A simple math operations package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/leonardosantosdev/simplemath_leonardosantosdev',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
