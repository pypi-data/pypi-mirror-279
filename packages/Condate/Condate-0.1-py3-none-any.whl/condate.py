import os
import platform
from datetime import datetime
import re

def clear_console():
    # Очистка консоли для Windows и Unix систем
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def remove_suffixes(date_str):
    # Удаляем суффиксы "st", "nd", "rd", "th"
    for suffix in ["st", "nd", "rd", "th"]:
        date_str = re.sub(r'(\d+)' + suffix, r'\1', date_str)
    return date_str

def extract_date(date_str):
    # Извлекаем дату из строки
    date_pattern = r'(\d{1,2}(?:st|nd|rd|th)?\s+of\s+\w+\s+\d{4}|\w+\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}|\d{1,2}\s+\w+\s*,\s*\d{4})'
    match = re.search(date_pattern, date_str)
    if match:
        return match.group(0)
    else:
        raise ValueError("Не удалось извлечь дату из строки")

def convert_date():
    print("Made by Avinion\nTelegram: @akrim\n")
    while True:
        # Запрашиваем у пользователя дату
        date_str = input("Введите дату для конвертации в числовой формат: ")
        
        try:
            # Извлекаем дату из строки
            date_extracted = extract_date(date_str)
            # Удаляем суффиксы
            date_str_clean = remove_suffixes(date_extracted.strip().replace(',', ''))
            
            # Проверяем наличие формата "Day of Month Year"
            if " of " in date_str_clean:
                date_obj = datetime.strptime(date_str_clean, "%d of %B %Y")
            else:
                parts = date_str_clean.split()
                # Проверяем если первый элемент это число, то формат "Day Month Year"
                if parts[0].isdigit():
                    date_obj = datetime.strptime(date_str_clean, "%d %B %Y")
                else:
                    # Формат "Month Day Year"
                    date_obj = datetime.strptime(date_str_clean, "%B %d %Y")
            
            # Форматируем дату в нужный формат "dd.mm.yyyy"
            formatted_date = date_obj.strftime("%d.%m.%Y")
            
            # Выводим результат
            print(f"Конвертированная дата: {formatted_date}")
        except ValueError:
            print("Неверный формат даты. Пожалуйста, попробуйте еще раз.")
        
        # Запрашиваем у пользователя, хочет ли он продолжить работу с скриптом
        continue_choice = input("Хотите продолжить? (y/n): ").strip().lower()
        
        if continue_choice == 'y':
            clear_console()
        elif continue_choice == 'n':
            break
        else:
            print("Неверный ввод. Завершаю работу.")
            break

if __name__ == "__main__":
    convert_date()
