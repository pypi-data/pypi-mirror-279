from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vidcomp",
    version="0.1",
    author="Avinion",
    author_email="shizofrin@gmail.com",
    description="A video comparison tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://twitter.com/Lanaev0li",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'vidcomp=vidcomp.main:main',
        ],
    },
)
