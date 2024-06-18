from setuptools import setup, find_packages

setup(
    name="liechains",
    version="0.4.0",
    author="leeliewhite",
    author_email="leeliewhite@gmail.com",
    description="toolkit for blockchains",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "web3",
        "websocket-client",
        "cryptography"
    ],
    python_requires=">=3.9",
)
