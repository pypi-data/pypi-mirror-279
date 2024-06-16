from setuptools import setup, find_packages
import tetx


setup(
    name='audio2vec',
    version='0.6.6',
    packages=find_packages(),
    url='https://github.com/dallo7/audio2Vec.git',
    author='Dalmas Chituyi',
    author_email='cwakhusama@gmail.com',
    description='An Audio2Vec annotation library',
    long_description=tetx.longtext,
    long_description_content_type='text/markdown',
    install_requires=["pandas>=2.0.1", "scikit-learn==1.4.0"]
)

