from setuptools import setup, find_packages

setup(
    name='EncryptDecryptPy',
    version='1.0.0',
    description='A Python package for encrypting and decrypting strings.',
    long_description='''This package provides a simple and secure way to encrypt and decrypt strings in Python. It is recommended to use a strong encryption library like cryptography for this purpose. This package requires cryptography to be installed separately.''',
    long_description_content_type="text/markdown",
    url='https://github.com/ShanKonduru/EncryptDecryptPy',  # Replace with your project URL
    author='Shan Konduru',
    author_email='ShanKonduru@gmail.com',
    packages=find_packages(),
    install_requires=[
        'cryptography'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
