import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

install_modules = ["evernote==1.25.3",
                   "enum34==1.1.10",
                   "cryptography==3.3.2",
                   "httplib2==0.20.2",
                   "ipaddress==1.0.23"
                   ]

setuptools.setup(
    name="evernote_cli",
    version="1.0.4",
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
    install_requires=install_modules,
    python_requires='>2.7, <3.0',
)
