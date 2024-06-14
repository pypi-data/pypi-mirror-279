from setuptools import find_packages, setup

# Read the requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    packages=find_packages(),
    install_requires=requirements,
)

