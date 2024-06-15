from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="api-kaede",
    version="V12",
    author="Kento Hinode",
    author_email="cleaverdeath@gmail.com",
    description="A Python package to interact with Kaede API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "patch-ng",  # Install patch-ng first
        "requests",
        "pillow",
        "paddlepaddle",
        "paddleocr",
        "yt-dlp", 
        "lmdb"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)