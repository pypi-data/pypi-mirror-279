from setuptools import setup, find_packages

setup(
    author= "Dear Norathee",
    description="package build on top of os and add more convient functionality",
    name="os_toolkit",
    version="0.1.2",
    packages=find_packages(),
    license="MIT",
    install_requires=["pandas","py_string_tool>=0.1.4", "python_wizard>=0.1.2",]

)