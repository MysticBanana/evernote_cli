import setuptools
import sys



with open("README.md", "r") as fh:
    long_description = fh.read()

install_modules = ["evernote", "cryptography", "enum34", "httplib2", "ipaddress"]

setuptools.setup(
    name="evernote_cli",
    version="1.0.3",
    author="Secret",
    author_email="no-reply@hs-mittweida.de",
    description="Package to create Hive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=install_modules,
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>2.7, <3.0',
)
