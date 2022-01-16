import setuptools
import sys



with open("README.md", "r") as fh:
    long_description = fh.read()

install_modules = ["evernote", "cryptography", "enum", "enum32", "httplib2", "ipaddress", "oauth2", "stdiomask", "Fernet"]

setuptools.setup(
    name="evernote_cli",
    version="1.0.1",
    author="Secret",
    author_email="no-reply@hs-mittweida.de",
    description="Package to create Hive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>2.7, <3.0',
)
