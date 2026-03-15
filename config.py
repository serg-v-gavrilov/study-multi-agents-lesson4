from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env"}

    api_key: SecretStr = Field(alias="openai_api_key")
    model_name: str = "gpt-5.4"

    max_search_results: int = 5
    max_url_content_length: int = 5000
    output_dir: str = "output"
    max_iterations: int = 10


Settings = Settings()

SYSTEM_PROMPT = "Ти - персональний асистент. " \
                "Отримуй запити від користувача, виконуй пошук інформації за допомогою доступних тобі інструментів. " \
                "Результат записуй у вигладі файлу у markdown-форматі. " \
                "Результат формуй українською мовою (для спеціальних термінів можна використовувати англійську)."
