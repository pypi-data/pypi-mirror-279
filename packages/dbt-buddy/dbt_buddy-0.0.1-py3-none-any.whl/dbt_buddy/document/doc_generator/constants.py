DOTENV_API_KEY_NAME: str = "API_KEY"
DOTENV_CATALOG_ID_NAME: str = "CATALOG_ID"

DBT_CODEGEN_MACRO: str = """
{{{{ codegen.generate_model_yaml(model_names=['{model}'], include_data_types=False) }}}}
"""
DBT_CLI_ARGS: list = [
    "--quiet",
    "--no-print",
    "compile",
]

GPT_BASE_URL: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
GPT_MODEL_URI: str = "gpt://{catalog_id}/yandexgpt"
GPT_TEMPERATURE: float = 0.3
GPT_MAX_TOKENS: str = "8000"
GPT_ANSWER_TEMPLATE: str = """
    [{"column_name": <название колонки>, "description": <описание колонки>, "possible_values": <возможные значения>},..]
"""
