from setuptools import setup, find_packages

# Project details
package_name = "gpt-ignore"
description = "A tool to manage `.gpt-ignore` files for excluding specific files from OpenAI GPT training data."
author = "Tayyip Canbay"
author_email = "tayyipcanbaydev@gmail.com"
url = "https://github.com/tayyipcanbay/gpt-ignore"
version = "0.1.0"

# Dependencies
requirements = ["os", "shutil", "argparse"]

setup(
    name=package_name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    packages=find_packages(exclude=["tests", "*.tests", "*.txt"]),
    install_requires=requirements,
)
