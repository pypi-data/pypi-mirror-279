from setuptools import setup, find_packages

setup(
    name="heep",
    version="1.0.0",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.abderrezzak@gmail.com",
    license="MIT",
    description="Sophisticate Heap",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/heep/",
    packages=find_packages(),
    install_requires=[
        "tabulate>=0.9.0",
    ],
    keywords=[
        "heap",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
