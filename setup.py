from setuptools import setup, find_packages
import nisanyan_cli

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as file:
    requires = [line.strip() for line in file.readlines()]

VERSION = "0.0.1"
DESCRIPTION = "CLI for nisanyansozluk.com (nis <word>)"

setup(
    name="nisanyan_cli",
    version=VERSION,
    url="https://github.com/agmmnn/nisanyan-cli",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="agmmnn",
    license="Apache License Version 2.0",
    license_files=["LICENSE"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    packages=["nisanyan_cli"],
    install_requires=requires,
    include_package_data=True,
    package_data={"nisanyan_cli": ["nisanyan_cli/*"]},
    python_requires=">=3.5",
    entry_points={"console_scripts": ["nis = nisanyan_cli.__main__:cli"]},
)
