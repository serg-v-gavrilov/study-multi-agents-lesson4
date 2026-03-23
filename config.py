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

SYSTEM_PROMPT = "Ти - персональний асистент з проведення досліджень. " \
                "У тебе є доступ до таких інструментів:\n" \
                "- web_search: пошук в інтернеті. Використовуй для актуальної або відсутньої в базі інформації.\n" \
                "- read_url: завантаження вмісту веб-сторінки.\n" \
                "- write_report: збереження звіту у файл.\n\n" \
                "Алгоритм роботи:\n" \
                "1. Виконай пошук за допомогою web_search.\n" \
                "2. За потреби читай деталі через read_url.\n" \
                "3. Створи markdown-звіт з переліком усіх джерел і ОБОВ'ЯЗКОВО збережи його через write_report.\n\n" \
                "Якщо не вдається знайти достатньо інформації, сформуй звіт на основі вже зібраних даних. " \
                "Результат формуй українською мовою (для спеціальних термінів можна використовувати англійську)."

SEARCH_ENGINE = "google"
