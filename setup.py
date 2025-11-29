"""
项目打包配置文件
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="audi-emotion",
    version="1.0.0",
    author="Qianyuqianxun",
    author_email="lizhuoqi25@tsinghua.edu.com",
    description="实时语音情感分析系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/audi-emotion",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "audi-emotion=project.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["resource/*.txt"],
    },
)

