from setuptools import setup, find_packages

setup(
    author= "Dear Norathee",
    description="package build on top of pandas and add more convient functionality. Make your code short and easy to read",
    name="dataframe_short",
    version="0.1.7",
    packages=find_packages(),
    license="MIT",
    install_requires=["pandas","os_toolkit","py_string_tool","datatable","polars","python_wizard","pyxlsb"],
    
 
)