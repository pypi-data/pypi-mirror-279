# setup.py
from setuptools import setup, find_packages

setup(
    name='data_science_test123',
    version='0.1.0',
    author='Ahmed',
    author_email='ahmed.asaad.refaei@gmail.com',
    description='A small example package for data science tools',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
