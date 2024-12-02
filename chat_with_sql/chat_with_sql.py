""" Main module for ChatWithSQL class. """

import re
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai import OpenAI
from llama_index.llms.llama_api import LlamaAPI
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from llama_index.readers.database import DatabaseReader
from llama_index.core.tools import ToolMetadata
from llama_index.core.selectors import LLMSingleSelector

# Constants for regular expressions and defaults
JSON_PATTERN = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def remove_json_parts(input_text: str) -> str:
    """Remove JSON parts enclosed in triple backticks."""
    return JSON_PATTERN.sub(r"\1", input_text)


def modify_sql_query_params(sql_query: str, params: List[Any]) -> str:
    """Replace placeholders in an SQL query with actual parameters."""
    for value in params:
        sql_query = sql_query.replace("?", str(value), 1)
    return sql_query


class ChatWithSQL:
    """
    Manages interaction between an LLM and an SQL database.
    """

    def __init__(
        self,
        database_url: str,
        llm: str,
        model: Optional[str] = "",
        llm_api_key: Optional[str] = None,
        query_schema: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Initialize ChatWithSQL instance.

        Args:
            database_url (str): Database connection URI.
            llm (str): Type of LLM ('gemini', 'openai', 'llama_api', 'ollama').
            model (str, optional): Model name for the LLM. Defaults to "".
            llm_api_key (str, optional): API key for accessing the LLM. Defaults to None.
            query_schema (List[Dict[str, Any]], optional): Schema for SQL queries. Defaults to None.
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Assign parameters
        self.database_url = database_url
        self.model = model
        self.llm_api_key = llm_api_key
        self.query_schema = query_schema or []

        # Initialize LLM and database reader
        self.llm = self._initialize_llm(llm)
        self.reader = DatabaseReader(uri=self.database_url)

        # Parse tool metadata and schema
        self.pool = [
            ToolMetadata(description=item["description"], name=item["name"])
            for item in self.query_schema
        ]
        self.pool_schema = [
            {"sql": item["sql"], "params": item["params"]} for item in self.query_schema
        ]

    @property
    def connection_info(self) -> str:
        """Retrieve database connection information."""
        return f"Database URL: {self.database_url}, Model: {self.model}"

    def _initialize_llm(self, llm: str):
        """Initialize LLM based on the specified type."""
        llm_classes = {
            "gemini": Gemini,
            "openai": OpenAI,
            "llama_api": LlamaAPI,
            "ollama": Ollama,
        }
        if llm in llm_classes:
            return llm_classes[llm](model=self.model, api_key=self.llm_api_key)
        raise ValueError(f"Unsupported LLM type: {llm}")

    def parse_json_string(self, json_string: str) -> Dict[str, Any]:
        """Parse a JSON string into a dictionary."""
        try:
            cleaned_json = remove_json_parts(json_string)
            return json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing error: {e}")
            return {}

    def parse_param_value(self, value: Any, expected_type: str) -> Optional[Any]:
        """Convert a value to the expected type."""
        try:
            if value is None:
                return None
            if expected_type == "date":
                return f"'{datetime.strptime(value, DATE_FORMAT).date()}'"
            if expected_type == "datetime":
                return f"'{datetime.strptime(value, DATETIME_FORMAT)}'"
            if expected_type == "int":
                return int(value)
            if expected_type == "float":
                return float(value)
            if expected_type == "str":
                return f"'{str(value)}'"
            self.logger.warning(f"Unsupported type: {expected_type}. Defaulting to str.")
            return str(value)
        except Exception as e:
            self.logger.error(f"Error parsing {value} to {expected_type}: {e}")
            return None

    def validate_params(self, params: Dict[str, Any], schema: Dict[str, Dict[str, Any]]) -> List[Any]:
        """Validate and sanitize parameters against a schema."""
        validated_params = []
        for key, rules in schema.items():
            expected_type = rules.get("type", "str")
            default_value = rules.get("default")
            parsed_value = self.parse_param_value(params.get(key, default_value), expected_type)
            validated_params.append(parsed_value if parsed_value is not None else default_value)
        self.logger.info(f"Validated parameters: {validated_params}")
        return validated_params

    def load_data(self, prompt: str) -> Dict[str, Any]:
        """
        Retrieve data from the database based on a user prompt.

        Args:
            prompt (str): The user's prompt.

        Returns:
            Dict[str, Any]: Retrieved data or an empty dictionary if an error occurs.
        """
        selector = LLMSingleSelector.from_defaults(llm=self.llm)

        try:
            selected_query = selector.select(self.pool, query=prompt)
            schema = self.pool_schema[selected_query.ind]
            sql_query = schema["sql"]

            if schema["params"]:
                param_keys = ", ".join(schema["params"].keys())
                prompt_message = (
                    f"Extract parameters ({param_keys}) from the context below:\n"
                    f"Context: {prompt}\n"
                    f"Format: JSON with dates as '{DATE_FORMAT}' and datetimes as '{DATETIME_FORMAT}'."
                )
                extraction_prompt = ChatMessage(role="user", content=prompt_message)
                parameter_data = self.llm.chat([extraction_prompt])
                final_params = self.parse_json_string(parameter_data.message.content)
                validated_params = self.validate_params(final_params, schema["params"])
                sql_query = modify_sql_query_params(sql_query, validated_params)

            documents = self.reader.load_data(query=sql_query)
            return {"results": [doc.text for doc in documents]}

        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            return {}
