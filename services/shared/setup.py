from setuptools import setup, find_packages

setup(
    name="shared",
    version="0.1.0-dev",
    packages=find_packages(),
    install_requires=["python-jose>=3.5.0", "fastapi>=0.115.12", "pydantic>=2.11.5"],
    python_requires=">=3.10",
)
