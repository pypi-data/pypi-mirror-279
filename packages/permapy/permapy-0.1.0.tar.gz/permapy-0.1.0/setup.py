from setuptools import setup, find_packages

setup(
    name="permapy",
    version="0.1.0",
    description="A Python package to interact with the Arweave network and Permaweb",
    author="Krish Soni",
    url="https://github.com/krishvsoni",
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
