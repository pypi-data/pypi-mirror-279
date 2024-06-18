from setuptools import setup, find_packages


setup(
    name="aisolutions",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[
        "openai",
        "requests",
        "dinjectorr",
    ],
    url="https://github.com/dmtno/aisolutions",
    license="MIT",
    author="DMYTRO IVANOV",
    author_email="dima.ivanov.py@gmail.com",
    description="AI Solutions",
)
