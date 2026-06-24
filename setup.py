from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smartclip",
    version="1.0.0",
    author="ZJJ50777",
    description="AI-Powered Clipboard Manager with local LLM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZJJ50777-UI/SmartClip",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=["pyperclip>=1.8.0", "requests>=2.28.0"],
    entry_points={
        "console_scripts": [
            "smartclip=smartclip.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Operating System :: OS Independent",
    ],
)
