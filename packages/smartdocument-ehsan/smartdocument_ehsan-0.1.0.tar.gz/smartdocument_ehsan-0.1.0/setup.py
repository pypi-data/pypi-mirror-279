from setuptools import setup, find_packages

setup(
    name="smartdocument_ehsan",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    author="ehsan125",
    author_email="ehsanpro94@gmail.com",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Ehsan125/smartdocument_ehsan",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
