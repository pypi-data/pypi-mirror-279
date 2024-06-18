# coding=utf-8

import os
import pathlib
import sys

sys.path.append(os.path.dirname(__file__))
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

install_requires = [
    "requests[socks]",
]

setup(
    name="openaichatlib",
    version="1.1.3",
    description="OpenAI Chat API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IAn2018cs/OpenAIChatLib",
    author="IAn2018",
    author_email="ian2018cs@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="openai, ChatGPT, api, chat",
    python_requires=">=3.9, <3.13",
    packages=find_packages(),
    install_requires=install_requires,
)
