import json
from pathlib import Path


def get_schema(schema_name):
    # Определяем путь к файлу схемы относительно текущего файла теста
    current_dir = Path(__file__).parent.resolve()
    schema_path = current_dir / f'{schema_name}.json'

    with open(schema_path) as file:
        return json.loads(file.read())
