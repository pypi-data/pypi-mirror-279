from setuptools import setup, find_packages
import tetx


setup(
    name='audio2vec',
    version='0.5.5',
    packages=find_packages(),
    url='https://github.com/dallo7/audio2Vec.git',
    license='License: GPL version 3, excluding DRM provisions',
    author='Dalmas Chituyi',
    author_email='cwakhusama@gmail.com',
    description='An Audio2Vec annotation library',
    long_description=tetx.longtext,
    long_description_content_type='text/markdown',
    install_requires=["setuptools==68.2.2", "pandas==2.1.1", "scikit-learn==1.5.0"],
)

