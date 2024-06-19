from setuptools import setup, find_packages

setup(
    name="thri",
    version="1.0.0",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.abderrezzak@gmail.com",
    license="MIT",
    description="Sophisticate Tree",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/thri/",
    packages=find_packages(),
    install_requires=[
        "tabulate>=0.9.0",
        "linkedit>=1.0.9",
    ],
    keywords=[
        "tree",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
