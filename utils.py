import os
import pandas as pd
from aiogram import Bot
from typing import List, Dict


async def save_excel_file(bot: Bot, file_path: str, upload_dir: str) -> str:
    file_name = os.path.basename(file_path)
    saved_path = os.path.join(upload_dir, file_name)
    await bot.download_file(file_path, saved_path)
    return saved_path


def is_valid_excel(file_path: str) -> bool:
    try:
        pd.read_excel(file_path)
        return True
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return False


def check_excel_structure(file_path: str) -> bool:
    try:
        df = pd.read_excel(file_path)
        required_columns = {'title', 'url', 'xpath'}
        return required_columns.issubset(df.columns)
    except Exception as e:
        print(f"Ошибка при проверке структуры файла: {e}")
        return False


def read_excel_data(file_path: str) -> List[Dict[str, str]]:
    df = pd.read_excel(file_path)
    return df.to_dict('records')
