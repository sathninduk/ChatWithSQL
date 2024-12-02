import unittest
from chat_with_sql import ChatWithSQL

LLM_API_KEY = ""
DATABASE_URL = ""


class TestChatWithSQL(unittest.TestCase):
    def setUp(self):
        self.query_schema = [
            {
                "description": "select the last order",
                "name": "last_order",
                "sql": "SELECT * FROM orders ORDER BY order_date DESC LIMIT 1",
                "params": {}
            },
            {
                "description": "select the first order",
                "name": "first_order",
                "sql": "SELECT * FROM orders ORDER BY order_date LIMIT 1",
                "params": {}
            },
            {
                "description": "select specific two orders by order number",
                "name": "specific_two_orders_by_number",
                "sql": "SELECT * FROM orders WHERE order_id = ? OR order_id = ? AND customer_id = ?",
                "params": {
                    "order_id_1": {"type": "int", "default": "*"},
                    "order_id_2": {"type": "int", "default": "*"},
                    "customer_id": {"type": "int", "default": 20}
                }
            },
            {
                "description": "select specific order by order date",
                "name": "specific_order_by_date",
                "sql": "SELECT * FROM orders WHERE order_date = '?'",
                "params": {
                    "order_date": {"type": "date", "default": "*"}
                }
            }
        ]
        self.chat_with_sql = ChatWithSQL(
            llm="gemini",
            model="models/gemini-pro",
            llm_api_key=LLM_API_KEY,
            database_url=DATABASE_URL,
            query_schema=self.query_schema
        )

    def test_initialization(self):
        self.assertEqual(self.chat_with_sql.database_url, DATABASE_URL)
        self.assertEqual(self.chat_with_sql.model, "models/gemini-pro")
        self.assertEqual(self.chat_with_sql.llm_api_key, LLM_API_KEY)
        self.assertEqual(len(self.chat_with_sql.pool), 4)
        self.assertEqual(len(self.chat_with_sql.pool_schema), 4)

    def test_connection_info(self):
        self.assertEqual(
            self.chat_with_sql.connection_info,
            f"Database URL: {DATABASE_URL}, Model: models/gemini-pro"
        )

    def test_parse_json_string(self):
        json_string = '''```json\n{"key": "value"}\n```'''
        result = self.chat_with_sql.parse_json_string(json_string)
        self.assertEqual(result, {"key": "value"})

    def test_parse_param_value(self):
        self.assertEqual(self.chat_with_sql.parse_param_value("2023-01-01", "date"), "'2023-01-01'")
        self.assertEqual(self.chat_with_sql.parse_param_value("2023-01-01 12:00:00", "datetime"),
                         "'2023-01-01 12:00:00'")
        self.assertEqual(self.chat_with_sql.parse_param_value("123", "int"), 123)
        self.assertEqual(self.chat_with_sql.parse_param_value("123.45", "float"), 123.45)
        self.assertEqual(self.chat_with_sql.parse_param_value("test", "str"), "'test'")

    def test_validate_params(self):
        params = {"order_id_1": 1, "order_id_2": 2, "customer_id": 30}
        schema = {
            "order_id_1": {"type": "int", "default": "*"},
            "order_id_2": {"type": "int", "default": "*"},
            "customer_id": {"type": "int", "default": 20}
        }
        result = self.chat_with_sql.validate_params(params, schema)
        self.assertEqual(result, [1, 2, 30])


if __name__ == "__main__":
    unittest.main()
