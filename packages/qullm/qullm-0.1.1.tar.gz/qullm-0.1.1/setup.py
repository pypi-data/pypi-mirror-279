from setuptools import setup, find_packages

setup(
    name='qullm',
    version='0.1.1',
    description='Simulation quantum neural network equation is used for large language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='C.C.K Leon',
    author_email='ckchau1@asu.edu',
    url='https://github.com/1nobodybutme1/qullm',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)