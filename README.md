# ChatWithSQL

**ChatWithSQL** is a Python library that bridges the gap between natural language queries and SQL databases. Designed for reliability, security, and performance, ChatWithSQL allows developers to leverage advanced Language Learning Models (LLMs) like OpenAI, Gemini, and more to retrieve database data using simple, intuitive natural language prompts.
![Banner.png](docs_src%2Fimages%2FBanner.png)

## 🎯 Why ChatWithSQL?

A major risk of Text-to-SQL systems is the potential execution of arbitrary SQL queries, which can result in **unauthorized data access, security vulnerabilities, inefficient query performance, or incorrect query results**. Common mitigations include using restricted roles, read-only databases, and sandboxed environments. However, ChatWithSQL takes this one step further.

ChatWithSQL has implemented a **schema-based validation approach** to ensure that only SQL queries adhering to a predefined schema are generated and executed. This mechanism restricts the scope of data retrieval strictly within the defined parameters, effectively mitigating the risks of arbitrary or malicious queries. Each query is validated against the schema before execution, **guaranteeing compliance and eliminating unauthorized access**.

This unique approach positions ChatWithSQL as a leader in secure and reliable, natural language-driven SQL data retrieval.

## 🚀 Key Features

* **Natural Language to SQL**: Translate human-readable prompts into actionable SQL queries.
* **Schema-Validated Queries**: Ensures only schema-defined queries are executed, mitigating arbitrary query risks.
* **LLM Flexibility**: Seamless integration with multiple LLMs (Gemini, OpenAI, Ollama, LlamaAPI).
* **Secure Execution**: Parameter validation and query sanitization to prevent SQL injection and unauthorized access.
* **Dynamic Query Parameter Handling**: Automatically extracts, validates, and maps parameters to SQL placeholders.
* **Database-Agnostic**: Compatible with any database supported by the URI connection format.
* **Comprehensive Logging**: Provides detailed logs for easier debugging and monitoring.

## 📦 Installation

You can install ChatWithSQL using pip:

```bash
pip install chatwithsql
```

## 🛠️ Setup and Usage

### 1. **Initialization**

```python
from chat_with_sql import ChatWithSQL

# Configuration
database_url = "your_database_url"
llm = "openai"  # Supported: gemini, openai, llama_api, ollama
model_name = "gpt-3.5-turbo"
api_key = "your_llm_api_key"
query_schema = [
    {
        "description": "Retrieve user data by user ID",
        "name": "get_user_data",
        "sql": "SELECT * FROM users WHERE id = ?",
        "params": {"id": {"type": "int", "default": None}},
    },
]

# Initialize ChatWithSQL
chat_with_sql = ChatWithSQL(
    database_url=database_url,
    llm=llm,
    model=model_name,
    llm_api_key=api_key,
    query_schema=query_schema,
)
```

### 2. **Executing Queries**

Use the `load_data` method to process a natural language prompt and retrieve data:

```python
prompt = "Show me the details of the user with ID 5."
response = chat_with_sql.load_data(prompt)
print(response)
```

## 🛡️ Security by Design

ChatWithSQL mitigates one of the largest risks of Text-to-SQL systems: **arbitrary query execution**. It employs schema-based validation to restrict query generation within pre-defined parameters. SQL queries are dynamically constructed and validated, ensuring:

1. Queries are limited to schema-defined structures.
2. Parameters are sanitized and validated against expected types.
3. Arbitrary query execution by LLMs is entirely eliminated.

## 🌐 Supported LLMs

* **OpenAI** (e.g., GPT-4, GPT-3.5)
* **Gemini**
* **LlamaAPI**
* **Ollama**

## 🧰 API Reference

### **ChatWithSQL**

#### Constructor

```python
ChatWithSQL(
    database_url: str,
    llm: str,
    model: Optional[str] = "",
    llm_api_key: Optional[str] = None,
    query_schema: Optional[List[Dict[str, Any]]] = None,
)
```

* **`database_url`**: Connection URI for the database.
* **`llm`**: Type of LLM to use (`gemini`, `openai`, `llama_api`, `ollama`).
* **`model`**: LLM model name.
* **`llm_api_key`**: API key for accessing the LLM.
* **`query_schema`**: List of schema definitions, each with `description`, `name`, `sql`, and `params`.

#### Method: `load_data(prompt: str) -> Dict[str, Any]`

Executes a natural language query and retrieves data.

* **`prompt`**: Natural language request.
* **Returns**: Query results as a dictionary.

## 📝 Query Schema Format

The `query_schema` parameter ensures secure and structured interactions. Each schema item includes:

* **`description`**: Human-readable description of the query.
* **`name`**: Unique name of the query.
* **`sql`**: SQL query template with placeholders (`?`) for parameters.
* **`params`**: Dictionary defining parameters with:
  * `type`: Data type (`str`, `int`, `float`, `date`, `datetime`).
  * `default`: Specify the default value for the parameter or if it can be any value, indicate it as null.

Example:

```json
[
    {
        "description": "Fetch user details by ID",
        "name": "get_user_details",
        "sql": "SELECT * FROM users WHERE id = ?",
        "params": {"id": {"type": "int", "default": null}}
    },
    {
        "description": "Fetch user details by DOB",
        "name": "get_user_details_by_dob",
        "sql": "SELECT * FROM users WHERE dob = ?",
        "params": {"dob": {"type": "date", "default": null}}
    }
]
```

## 🗺️ Architecture
![architecture-diagram.png](docs_src%2Fimages%2Farchitecture-diagram.png)


## 🐛 Logging and Debugging

ChatWithSQL includes extensive logging for better observability:

* Logs parameter validation errors.
* Logs malformed prompts or unexpected results from the LLM.
* Tracks query construction and database execution.

Enable logging by configuring Python’s `logging` module.

## 🏗️ Contributing

Contributions are welcome! Please submit a pull request or open an issue on our [GitHub Repository](https://github.com/sathninduk/ChatWithSQL).

## 📜 License

ChatWithSQL is open-source software licensed under the MIT License.

## 🤝 Support

If you have any questions or issues, feel free to contact us at [hello@bysatha.com](mailto:hello@bysatha.com) or open a GitHub issue.
