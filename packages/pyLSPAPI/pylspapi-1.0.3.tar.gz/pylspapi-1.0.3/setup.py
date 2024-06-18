from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyLSPAPI",
    version="1.0.3",
    author="Leo Aqua",
    author_email="contact@leoaqua.de",
    description="Python API for Leitstellenspiel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Leo-Aqua/LSPAPI",
    keywords=["Leitstellenspiel", "API", "LSPAPI", "LSS", "API"],
    install_requires=[
        "pytest-playwright",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
