from setuptools import setup, find_packages

setup(
    name="nyogyi_pretty_xml",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "lxml",
    ],
    entry_points={
        'console_scripts': [
            'nyogyi-pretty-xml=nyogyi_pretty_xml.nyogyi_pretty_xml:main',
        ],
    },
    author="Thein Htike Nyo",
    author_email="theinhtitenyo@gmail.com",
    description="A script to pretty print large XML files",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://pypi.org/project/nyogyi-pretty-xml/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
