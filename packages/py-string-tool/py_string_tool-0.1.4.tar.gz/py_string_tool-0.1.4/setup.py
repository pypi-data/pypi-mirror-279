from setuptools import setup, find_packages

setup(
    author= "Dear Norathee",
    description="useful additional string functions",
    name="py_string_tool",
    version="0.1.4",
    packages=find_packages(),
    license="MIT",
    install_requires=["thefuzz","langdetect","pandas","python_wizard>=0.1.1","python-Levenshtein"],

)