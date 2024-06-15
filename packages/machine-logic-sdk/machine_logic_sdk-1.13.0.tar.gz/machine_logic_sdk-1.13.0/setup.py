# type: ignore
"""Setup script for the Vention Python SDK for Vention hardware.

This script uses setuptools to package the SDK, making it easy to distribute and install.
"""
from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="machine-logic-sdk",
    version="1.13.0",
    description="SDK for controlling Vention hardware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://vention.io/resources/guides/machinelogic-python-programming-514",
    author="VentionCo",
    author_email="vention-sw-ci@vention.cc",
    packages=find_packages(exclude=["qa*", "tests*"]),
    install_requires=[
        "miros==4.2.1",
        "paho-mqtt==1.5.1",
        "types-requests==2.28.11",
        "requests==2.31.0",
        "typing_extensions==4.6.3",
        "parameterized",
        "numpy==1.24.2",
        "roslibpy==1.4.2",
        "scipy==1.11.1",
        "zope.interface==5.5.2",
    ],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
    ],
    python_requires=">=3.6",
)
