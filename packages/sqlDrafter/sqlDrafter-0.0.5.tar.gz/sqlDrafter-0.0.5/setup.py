import os
from setuptools import find_packages, setup




def package_files(directory):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths




setup(
    name="sqlDrafter",
    packages=find_packages(),
    version="0.0.5",
    description="sqldrafter is a Python library that helps you generate data queries from natural language questions.",
    author="yanQiao",
    license="Apache License,Version 2.0",
    install_requires=[
        "requests>=2.28.2",
        "prompt-toolkit>=3.0.38",
        "fastapi",
        "uvicorn",
        "tqdm",
        "pwinput",
        "mysql-connector-python",
        "sasl",
        "thrift",
        "thrift-sasl",
        "PyHive"
    ],
    entry_points={
        "console_scripts": [
            "sqlDrafter=sqldrafter.cli:main",
        ],
    },
    author_email="xiaoyan@sqldrafter.com",
    url="https://www.sqldrafter.com",
    long_description="sqldrafter is a Python library that helps you generate data queries from natural language questions.",
    long_description_content_type="text/markdown",

)
