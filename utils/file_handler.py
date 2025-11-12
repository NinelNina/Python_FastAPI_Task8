import json
import os
from datetime import datetime
from typing import Dict, Any
import uuid

DATA_DIR = "data"


def ensure_data_dir():
    """Создает директорию для данных, если она не существует"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_appeal_to_json(appeal_data: Dict[str, Any]) -> str:
    """
    Сохраняет обращение в JSON-файл
    """
    ensure_data_dir()

    # Генерируем уникальный ID
    appeal_id = str(uuid.uuid4())

    # Добавляем метаданные
    appeal_record = {
        "id": appeal_id,
        "appeal_data": appeal_data,
        "created_at": datetime.now().isoformat()
    }

    # Сохраняем в файл
    filename = f"{DATA_DIR}/appeal_{appeal_id}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(appeal_record, f, ensure_ascii=False, indent=2)
        return appeal_id
    except Exception as e:
        raise Exception(f"Ошибка сохранения файла: {str(e)}")


def get_appeal_by_id(appeal_id: str) -> Dict[str, Any]:
    """
    Получает обращение по ID
    """
    filename = f"{DATA_DIR}/appeal_{appeal_id}.json"

    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Ошибка чтения файла: {str(e)}")