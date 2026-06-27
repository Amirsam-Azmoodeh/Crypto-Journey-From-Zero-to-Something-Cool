"""
Setup configuration for Crypto-Journey package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crypto-journey",
    version="2.0.0",
    author="Amirsam Azmoodeh",
    author_email="amirsamazmoodeh@gmail.com",
    description="A 26-step educational journey from basic XOR to Cuckoo Filters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crypto-journey",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security :: Cryptography",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=[
        "bitarray>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
            "ipython>=8.0.0",
            "pre-commit>=3.0.0",
        ],
        "benchmark": [
            "pytest-benchmark>=4.0.0",
        ],
    },
)