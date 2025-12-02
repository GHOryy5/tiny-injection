from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tiny-injection",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI Security Testing Framework with XDR Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tiny-injection",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/tiny-injection/issues",
        "Documentation": "https://yourusername.github.io/tiny-injection/",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tinyinject=tinyinject:main",
            "tiny-hunt=hunt_ai.py:main",
            "tiny-xdr=integrate_xdr.py:main",
        ],
    },
    include_package_data=True,
    package_data={
        "tiny_injection": [
            "data/payloads/*.txt",
            "config.yaml",
            ".env.example",
        ],
    },
)
