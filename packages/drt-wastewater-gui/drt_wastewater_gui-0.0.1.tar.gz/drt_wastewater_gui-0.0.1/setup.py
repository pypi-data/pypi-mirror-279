import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drt-wastewater-gui",
    version="0.0.1",
    author="Dmitry Trokhachev",
    author_email="dimiaa573@gmail.com",
    description="Tool for calculate wastewater dilution rate using Karaushev's method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
       'numpy',
    ],
    python_requires=">=3.8",
)