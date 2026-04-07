from setuptools import setup, find_packages

setup(
    name="mtdsim",
    version="0.2.0",
    packages=find_packages(),
    package_data={
        "mtdsim.data": ["*.txt"],
    },
    python_requires=">=3.9",
)
