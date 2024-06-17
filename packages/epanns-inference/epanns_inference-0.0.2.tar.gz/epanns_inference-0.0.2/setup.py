import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epanns_inference",
    version="0.0.2",
    author="Arshdeep-Singh-Boparai, Stefano Giacomelli (Ph.D. student UnivAQ)",
    author_email="arshdeep.singh@surrey.ac.uk, stefano.giacomelli@graduate.univaq.it",
    description="epanns_inference: EPANNs audio tagging inference api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StefanoGiacomelli/epanns_inference",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'torch', 'torchlibrosa'],
    python_requires='>=3.6',
)
