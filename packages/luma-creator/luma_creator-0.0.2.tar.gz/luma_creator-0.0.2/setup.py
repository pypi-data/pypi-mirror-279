from setuptools import find_packages, setup

setup(
    name="luma-creator",
    version="0.0.2",
    author="danaigc, yihong0618",
    author_email="zouzou0208@gmail.com",
    description="High quality video generation by https://lumalabs.ai/. Reverse engineered API.",
    url="https://github.com/yihong0618/LumaDreamCreator",
    install_requires=[
        "requests",
        "fake-useragent",
    ],
    packages=find_packages(),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["luma = luma.luma:main"],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
