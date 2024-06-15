from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8") as fh:
	long_description=fh.read()

setup(
name="math_and_points",
version="0.1.0",
packages=find_packages(),
install_requires=[],
author="Lucas Gongora",
description="Operaciones basicas con dos o mas numeros, y por otra partes operaciones con puntos en dos dimensiones",
long_description=long_description,
long_description_content_type="text/markdown",
url="",
)
