from setuptools import setup, find_packages

setup(
    name="find-and-replace-strings",
    version="1.0.0",
    description="Python package and pre-commit-hook for finding and replacing string(s) in file(s).",
    author="OpenCEPK Open Cloud Engineering Platform Kit",
    author_email="opencepk@gmail.com",
    python_requires=">=3.7",
    packages=find_packages(include=["find_and_replace", "find_and_replace.*"]),
    entry_points={
        "console_scripts": [
            "find-and-replace-strings=find_and_replace.main:main",
        ],
    },
)