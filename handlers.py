import os
from aiogram import types, F, Dispatcher
from aiogram.filters import Command
from database import insert_data
from utils import save_excel_file, is_valid_excel, check_excel_structure, read_excel_data
from settings import UPLOAD_DIR

# Директория для сохранения файлов хранится в настройках проекта

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def register_handlers(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    dp.message.register(handle_document, F.document)


async def start(message: types.Message):
    # Создаем клавиатуру с кнопкой
    await message.answer("Загрузите Excel файл.")


async def handle_document(message: types.Message):
    if message.document.mime_type in [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel']:
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path

        # Сохраняем файл
        saved_path = await save_excel_file(message.bot, file_path, UPLOAD_DIR)

        # Проверяем формат файла
        if not is_valid_excel(saved_path):
            await message.answer(
                "Ошибка: файл не является корректным Excel-файлом.")
            os.remove(saved_path)
            return

        # Проверяем структуру файла
        if not check_excel_structure(saved_path):
            await message.answer(
                "Ошибка: структура файла не соответствует ожидаемой.")
            os.remove(saved_path)
            return

        # Читаем данные из файла
        data = read_excel_data(saved_path)

        # Добавляем данные в базу данных
        added_rows = insert_data(data)

        # Отправляем пользователю добавленные строки
        if added_rows:
            response = "Добавленные строки:\n"
            for row in added_rows:
                response += f"title: {row['title']}, url: {row['url']}, xpath: {row['xpath']}\n"
            await message.answer(response)
        else:
            await message.answer(
                "Ошибка: не удалось добавить данные в базу данных.")

        # Удаляем файл после обработки
        os.remove(saved_path)
    else:
        await message.answer(
            "Ошибка: загруженный файл не является Excel таблицей.")
