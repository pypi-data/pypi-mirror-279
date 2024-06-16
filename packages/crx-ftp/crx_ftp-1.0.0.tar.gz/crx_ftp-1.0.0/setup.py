from setuptools import setup, find_packages

setup(
    name="crx-ftp",
    version="1.0.0",
    description="This library is designed for your own use.",
    long_description="This library is designed for your own use.",
    url="https://discord.gg/EEp67FWQDP",
    author="CRX-DEV",
    author_email="cherniq66@gmail.com",
    license="MIT License",
    

    packages=find_packages(include=['crxftp', 'crxftp.*']),
    install_requires=[
        "aioftp==0.22.3"
    ]
)
