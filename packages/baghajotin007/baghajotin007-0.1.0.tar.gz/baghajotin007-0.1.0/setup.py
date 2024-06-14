
### setup.py


from setuptools import setup, find_packages

setup(
    name="baghajotin007",
    version="0.1.0",
    author="Swaranjit",
    author_email="dextersaran@gmail.com",
    description="A simple Python package for basic arithmetic operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Swaran66/EcoSalinity",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
