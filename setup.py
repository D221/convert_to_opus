import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="convert_to_opus",
    version="0.0.1",
    author="D221",
    description="A simple python GUI tool that converts directory of audio files to opus",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/D221/convert_to_opus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
)