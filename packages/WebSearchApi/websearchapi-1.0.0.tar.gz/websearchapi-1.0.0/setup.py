
from setuptools import setup, find_packages

setup(
    name="WebSearchApi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Sharandeep Singh",
    author_email="notsharry2@gmail.com",
    description="A Python wrapper for the search API.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ConsiousAI/WebSearchApi-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
