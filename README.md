# ChatWithSQL

One of the major risks associated with Text-to-SQL systems is the potential for executing arbitrary SQL queries, which can lead to unauthorized data access or security breaches. Common mitigations include using restricted roles, read-only databases, and sandboxed environments. However, ChatWithSQL takes this one step further.

ChatWithSQL has implemented a schema-based validation approach to ensure that only SQL queries adhering to a predefined schema are generated and executed. This mechanism restricts the scope of data retrieval strictly within the defined parameters, effectively mitigating the risks of arbitrary or malicious queries. Each query is validated against the schema before execution, guaranteeing compliance and eliminating unauthorized access.

This unique approach positions ChatWithSQL as a leader in secure and reliable, natural language-driven SQL data retrieval.

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
