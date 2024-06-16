from setuptools import setup, find_packages

setup(
    name='matching-statistics',
    version='0.1.0',
    description='Library for Matching Statistics using Suffix Tree',
    author='Mihir Kestur',
    author_email='mkestur@cs.stonybrook.edu',
    packages=find_packages(),
    url="https://github.com/mihirkestur/matching-statistics",
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
