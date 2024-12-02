from setuptools import setup, find_packages

setup(
    name="chat_with_sql",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "llama-index",
        "fastapi",
        "pydantic",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library to manage interaction between an LLM and an SQL database.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chat_with_sql",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)