import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

with open("./README.md", "r") as rm:
    long_description = rm.read()

setup(
    name="pylookout",
    version="0.1.0",
    description="Simple Linux system monitoring tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lab-Brat/pyLookout",
    author="Lab-Brat",
    author_email="labbrat_social@pm.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Linux",
    ],
    packages=find_packages(),
    scripts=[
        "main.py",
        "info_collector.py",
        "lookout.py",
    ],
    install_requires=[
        "psutil",
        "sendgrid",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pylookout = main:main",
        ],
    },
)
