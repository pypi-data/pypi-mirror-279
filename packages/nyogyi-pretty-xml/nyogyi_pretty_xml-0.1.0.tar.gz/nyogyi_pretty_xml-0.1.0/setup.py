from setuptools import setup, find_packages

setup(
    name="nyogyi_pretty_xml",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "lxml",
    ],
    entry_points={
        'console_scripts': [
            'nyogyi-pretty-xml=nyogyi_pretty_xml.nyogyi_pretty_xml:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A script to pretty print large XML files",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/nyogyi_pretty_xml",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
