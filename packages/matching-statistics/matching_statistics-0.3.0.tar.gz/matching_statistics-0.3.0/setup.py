from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='matching-statistics',
    version='0.3.0',
    description='Library for Matching Statistics using Suffix Tree',
    author='Mihir Kestur',
    author_email='mkestur@cs.stonybrook.edu',
    long_description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/mihirkestur/matching-statistics",
    install_requires=[
        'suffix-trees',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
