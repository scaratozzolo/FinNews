import setuptools
import FinNews

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FinNews",
    version=FinNews.__version__,
    author="Scott Caratozzolo",
    author_email="scaratozzolo12@gmail.com",
    description="Package for gathering financial news from various RSS feeds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scaratozzolo/FinNews",
    package_data = {'FinNews': ['rss.db']},
    packages=setuptools.find_packages(),
    install_requires=["feedparser", "sqlite3", "pandas"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ],
)
