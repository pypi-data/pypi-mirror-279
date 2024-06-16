from setuptools import setup, find_packages

import read

setup(
    name='audio2vec',
    version='0.6.14',
    packages=find_packages(),
    url='https://github.com/dallo7/audio2Vec.git',
    license='GPL version 3, excluding DRM provisions',
    author='Dalmas Chituyi',
    author_email='cwakhusama@gmail.com',
    description='An Audio2Vec annotation library',
    long_description=read.read,
    long_description_content_type='text/markdown',
    install_requires=[
        "setuptools",
        "pandas",
        "scikit-learn"
    ],
)

