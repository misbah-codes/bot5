#!/usr/bin/env python3
"""
Setup script for NSAKCET College Chatbot
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nsakcet-chatbot",
    version="1.1.0",
    author="NSAKCET Development Team",
    author_email="info@nsakcet.ac.in",
    description="AI-powered chatbot for Nawab Shah Alam Khan College of Engineering and Technology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/nsakcet-chatbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "nsakcet-chatbot=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.html", "*.css", "*.js"],
    },
    keywords="chatbot, education, college, nlp, flask, nsakcet",
    project_urls={
        "Bug Reports": "https://github.com/your-username/nsakcet-chatbot/issues",
        "Source": "https://github.com/your-username/nsakcet-chatbot",
        "Documentation": "https://github.com/your-username/nsakcet-chatbot#readme",
    },
)
