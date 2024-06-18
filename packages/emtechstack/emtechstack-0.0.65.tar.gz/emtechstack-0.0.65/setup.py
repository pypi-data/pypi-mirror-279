from setuptools import setup, find_packages

setup(
    name="emtechstack",
    version="0.0.65",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "black",
        "requests",
        "tabulate",
        "termcolor",
    ],
    entry_points={
        "console_scripts": [
            "emtechstack=emtechstack.cli:cli",
            "e9k=emtechstack.cli:cli",
        ],
    },
)
