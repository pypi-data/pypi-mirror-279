from setuptools import setup, find_packages

setup(
    name="versacorellmchatapi",
    version="0.1.3",
    description="A Python library for interacting with the VersaCore LLM Chat API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jansen Tang",
    author_email="jansen.tang@ai-sherpa.io",
    url="https://github.com/AI-Sherpa/versacorellmchatapi",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
