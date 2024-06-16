from setuptools import setup, find_packages

setup(
    name="TesAPI",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author="Tes",
    author_email="antoshaspr@vk.com",
    description="TesAPI Client, and etc.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)