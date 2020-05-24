import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FinNews",
    version="0.1.1",
    author="Scott Caratozzolo",
    author_email="scaratozzolo12@gmail.com",
    description="Package for gathering financial news from various RSS feeds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scaratozzolo/FinNews",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ),
)
