from setuptools import setup, find_packages

setup(
    name="lstack",
    version="1.0.5",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.abderrezzak@gmail.com",
    license="MIT",
    description="Sophisticate Stack",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/lstack/",
    packages=find_packages(),
    install_requires=[
        "tabulate>=0.9.0",
        "linkedit>=1.0.9",
    ],
    keywords=[
        "stack",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
