from setuptools import setup, find_packages

setup(
    name="chatwithsql",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "llama-index",
        "llama-index-readers-database",
        "llama-index-llms-openai",
        "llama-index-llms-gemini",
        "llama-index-llms-llama-api",
        "llama-index-llms-ollama",
        "python-dotenv",
        "psycopg2"
    ],
    author="Sathnindu Kottage",
    author_email="hello@bysatha.com",
    description="ChatWithSQL: Secure, Schema-Validated Text-to-SQL, Eliminating Arbitrary Query Risks from LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sathninduk/ChatWithSQL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)