from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8") as fh:
	long_description=fh.read()

setup(
name="math_and_points",
version="0.1.3",
packages=find_packages(),
install_requires=[],
author="Lucas Gongora",
description="Operaciones básicas con dos o más números y, por otra parte, operaciones con puntos en dos dimensiones.",
long_description=long_description,
long_description_content_type="text/markdown",
url="",
)
