from setuptools import setup, find_packages
from pathlib import Path

package_directory = "algebraic_hbm"
requirements_filename = "requirements.txt"
readme_pypi = "README_pypi.md"

# Load README.
path = Path.joinpath(Path.cwd(), readme_pypi)
print(path)
with open(path) as file:
	readme = file.read()

# Load requirements.
path = Path.joinpath(Path.cwd(), package_directory, requirements_filename)
with open(path) as file:
	requirements = []
	for line in file.readlines():
		l = line.strip().split("=")
		l = l[0] + ">=" + l[-1]
		requirements.append(l)

setup(
	name=package_directory,
	version="0.1.4",
	author="Hannes Dänschel",
	author_email="daenschel@math.tu-berlin.de",
	description="Python implementation of the algebraic harmonic balance method for second order ordinary differential equations with polynomial coefficients.",
	long_description=readme,
	long_description_content_type='text/markdown',
	url="https://git.tu-berlin.de/hannes.daenschel/algebraic-hbm",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.10',
	install_requires=requirements,
)