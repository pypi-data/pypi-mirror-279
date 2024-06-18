import setuptools
import os


with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join("thin_lens", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")

setuptools.setup(
    name="thin_lens",
    version=version,
    description=("Compute the optics of the 'thin'-lens-equation."),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/thin_lens",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    packages=[
        "thin_lens",
    ],
    package_data={"thin_lens": []},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
