import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="firmware-collector-Grotax",
    version="0.0.1",
    author="Benjamin Brahmer",
    author_email="info@b-brahmer.de",
    description="Collecting Freifunk firmware from the GitHub API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ffsh/firmware-collector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)
