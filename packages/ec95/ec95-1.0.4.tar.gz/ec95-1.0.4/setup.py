from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


def parse_requirements(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()


setup(
    name="ec95",
    version="1.0.4",
    author="qdzzzxc",
    description="xD",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pyperclip>=1.8.2",
        "joblib>=1.4.2",
        "scipy>=1.13.1",
        "threadpoolctl>=3.5.0",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="example python",
    python_requires=">=3.7",
)
