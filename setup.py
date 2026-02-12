"""
Data Mesh Implementation Framework
A comprehensive framework for implementing Data Mesh architecture
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="data-mesh-framework",
    version="1.0.0",
    author="Gabriel Demetrios Lafis",
    author_email="",
    description="A comprehensive framework for implementing Data Mesh architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galafis/data-mesh-implementation-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    keywords="data-mesh, data-architecture, data-products, domain-driven-design",
    project_urls={
        "Bug Reports": "https://github.com/galafis/data-mesh-implementation-framework/issues",
        "Source": "https://github.com/galafis/data-mesh-implementation-framework",
        "Documentation": "https://github.com/galafis/data-mesh-implementation-framework/blob/main/README.md",
    },
)
