import os
from typing import List, Set
from pathlib import Path
from setuptools import setup, find_packages

ROOT_DIR = Path(__file__).resolve().parent

def get_path(*filepath) -> str:
    return ROOT_DIR.joinpath(*filepath)

def get_requirements() -> List[str]:
    """Get Python package dependencies from requirements.txt."""

    requirements_path = get_path("requirements.txt")
    if not requirements_path.is_file():
        raise FileNotFoundError(f"No such file: {requirements_path}")
    with requirements_path.open() as f:
        requirements = f.read().strip().split("\n")
    return requirements

setup(
    name='budserve',
    version='0.0.1',
    description='A client package to directly integrate Bud Serve engine to your python application.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BudEcosystem/bud-serve-sdk',
    packages=find_packages(include=['budserve', 'budserve.*']),
    install_requires=get_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
