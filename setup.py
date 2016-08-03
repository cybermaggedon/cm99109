import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cm99109", # Replace with your own username
    version="0.1",
    author="Cybermaggedon",
    author_email="mark@cyberapocalypose.co.uk",
    description="Virtual 8-bit microcontroller emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cybermaggedon/cm99109",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=[
        "scripts/cm99109-as",
        "scripts/cm99109-dis",
        "scripts/cm99109-exec",
        "scripts/cm99109-prog",
        "scripts/cm99109-to-js",
        "scripts/cm99109-upload",
        "scripts/cm99109-validate"
    ]
)
