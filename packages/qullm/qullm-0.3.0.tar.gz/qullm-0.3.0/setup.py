# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qullm",
    version="0.3.0",
    author="C.C.K Leon",
    author_email="ckchau1@asu.edu",
    description="A Python package for preprocessing and augmenting data for large language models by quantum Neural networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1nobodybutme1/qullm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "pandas",
    ],
    entry_points={
        'console_scripts': [
            'llm_data_processor=llm_data_processor.__main__:main',
        ],
    },
    include_package_data=True
)