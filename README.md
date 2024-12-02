# ChatWithSQL

ChatWithSQL is a Python library to manage interaction between a Large Language Model (LLM) and an SQL database.

## Installation

```bash
pip install chat_with_sql
```

## Usage

```python
from chat_with_sql import ChatWithSQL

# Initialize ChatWithSQL
chat_with_sql = ChatWithSQL(
    database_url="your_database_url",
    llm="gemini",
    model="models/gemini-pro",
    llm_api_key="your_llm_api_key",
    query_schema=query_schema
)

# Load data based on a prompt
data = chat_with_sql.load_data(prompt="your_prompt")
print(data)
```

## License
MIT License