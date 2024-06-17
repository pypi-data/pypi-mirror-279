from setuptools import setup, find_packages

setup(
    name='emtechstack',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'emtechstack=emtechstack.cli:cli',
        ],
    },
)
