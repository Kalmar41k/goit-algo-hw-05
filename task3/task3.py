"""
Модуль для обробки логів.

Цей модуль містить функції для зчитування, парсингу та аналізу лог-файлів.
Він дозволяє підраховувати кількість логів за рівнями, фільтрувати 
їх та виводити у табличному форматі.

Функції:
- parse_log_line(line: str) -> dict
- load_logs(file_path: str) -> list[dict]
- filter_logs_by_level(logs: list[dict], level: str) -> list[dict]
- count_log_by_level(logs: list[dict]) -> dict
- display_log_counts(counts: dict)
- main()
"""
import sys
from pathlib import Path
from collections import Counter

def parse_log_line(line: str) -> dict:
    """
    Парсить рядок лог-файлу на окремі компоненти.

    Параметри:
    ----------
    line : str
        Рядок з лог-файлу, який містить дату, час, рівень логування та текст повідомлення.

    Повертає:
    ---------
    dict
        Словник, що містить:
        - 'date_time': поєднана дата та час (str)
        - 'level': рівень логування (str)
        - 'text': текст повідомлення (str)
    """
    date, time, level, *text = line.split()
    date_time = date + " " + time
    text = " ".join(text)
    parsed_line = {
        "date_time": date_time,
        "level": level,
        "text": text
    }
    return parsed_line

def load_logs(file_path: str) -> list[dict]:
    """
    Зчитує лог-файл та парсить його рядки.

    Параметри:
    ----------
    file_path : str
        Шлях до лог-файлу, який потрібно зчитати.

    Повертає:
    ---------
    list[dict]
        Список словників, де кожен словник представляє парсений рядок лог-файлу.
        Якщо файл не знайдено або сталася помилка, повертає пустий список.
    """
    try:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"The file {file_path} does not exist or is not a file.")

        parsed_lines = []

        with open(file_path) as file:
            lines = file.readlines()

        parsed_lines.extend(parse_log_line(line.strip()) for line in lines)
        return parsed_lines

    except FileNotFoundError as e:
        print(e)
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def filter_logs_by_level(logs:list[dict], level: str) -> list[dict]:
    """
    Фільтрує лог-файли за заданим рівнем.

    Параметри:
    ----------
    logs : list[dict]
        Список парсених логів, які потрібно фільтрувати.
    level : str
        Рівень логування, за яким потрібно фільтрувати (INFO, ERROR, DEBUG, WARNING).

    Повертає:
    ---------
    list[dict]
        Список словників, що містять лише лог-файли з заданим рівнем.
    """
    filtered_list = []
    for log in logs:
        if level.upper() == log["level"]:
            filtered_list.append(log)
    return filtered_list


def count_log_by_level(logs: list[dict]) -> dict:
    """
    Підраховує кількість логів за рівнями.

    Параметри:
    ----------
    logs : list[dict]
        Список парсених логів, для яких потрібно виконати підрахунок.

    Повертає:
    ---------
    dict
        Словник, де ключами є рівні логування, а значеннями - кількість появ кожного рівня.
    """
    counted_levels = Counter()

    for log in logs:
        level = log.get("level")
        counted_levels[level] += 1

    return dict(counted_levels)

def display_log_counts(counts: dict):
    """
    Виводить таблицю з кількістю логів за рівнями в консоль.

    Параметри:
    ----------
    counts : dict
        Словник, де ключами є рівні логування, а значеннями - кількість появ кожного рівня.
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for k, v in counts.items():
        print(f"{k:<16} | {v}")

def main():
    """
    Головна функція програми, яка виконує зчитування лог-файлу, 
    підрахунок логів за рівнями та їх фільтрацію, якщо вказано.

    Вхідні параметри:
    ------------------
    Використовує параметри командного рядка для отримання шляху до файлу логів 
    та необов'язкового рівня логування для фільтрації.
    """
    if len(sys.argv) < 2:  # Перевірка на кількість аргументів
        print("Usage: python script.py <file_path> [level]")
        return

    file_path = sys.argv[1]
    level = ""

    if len(sys.argv) == 3:
        level = sys.argv[2]

    logs = load_logs(file_path)
    if not logs:
        print("No logs to display.")
        return

    display_log_counts(count_log_by_level(logs))

    if level != "":
        filtered_logs = filter_logs_by_level(logs, level)
        print(f"\nДеталі логів для рівня '{level}'")
        for log in filtered_logs:
            print(f"{log['date_time']} - {log['text']}")

if __name__ == "__main__":
    main()
