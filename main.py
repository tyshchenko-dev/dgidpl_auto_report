import questionary
import emoji
import re
from report import generate_report
import logging
import config


def mode_one():
    logging.info(f"{emoji.emojize(':hammer_and_wrench:')} Обрано режим 1: Створення звіту на основі всіх файлів.")
    generate_report()


def mode_two():
    logging.info(f"{emoji.emojize(':bar_chart:')} Обрано режим 2: Створення звіту по даті і області.")

    regions = ["Крим", "Вінницька", "Волинська", "Дніпропетровська", "Донецька", "Житомирська", "Закарпатська",
               "Запорізька", "Івано-Франківська", "Київська", "Кіровоградська", "Луганська", "Львівська",
               "Миколаївська", "Одеська", "Полтавська", "Рівненська", "Сумська", "Тернопільська", "Харківська",
               "Херсонська", "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська", "Київ", "Севастополь"]

    selected_regions = questionary.checkbox(
        "Оберіть області для звіту, можна обрати відразу декілька областей:",
        choices=regions
    ).ask()

    if not selected_regions:
        logging.info("Ви нічого не обрали. Програма завершена.")
        return

    region_pattern = r"\d{2}\_\d{4}\-\d{2}\_\d{4}"

    while True:
        date = input("Введіть місяць та рік на основі яких формувати звіт в форматі 01_2025-05_2025: ")
        if re.fullmatch(region_pattern, date):
            break
        else:
            logging.info("Ви ввели дані у невірному форматі. Спробуйте ще раз.")

    settings = {
        "selected_regions": selected_regions, "date": date
    }

    generate_report(settings)


def main():
    config.setup_logging()
    greeting = [
        f"{emoji.emojize(':police_officer:')} Привіт, це скрипт який допомагає зформувати статистику затримань по всій Україні.",
        f"{emoji.emojize(':classical_building:')} Розроблений для Департаменту головної інспекції та дотримання прав людини."
    ]
    logging.info(greeting[0])  # show message 1
    logging.info(greeting[1])  # show message 2

    choice = questionary.select(
        "Оберіть режим роботи скрипта:",
        choices=[
            "Звіт на основі всіх файлів",
            "Звіт по даті і області",
            "Завершити роботу"
        ]).ask()

    if choice == "Звіт на основі всіх файлів":
        mode_one()
    elif choice == "Звіт по даті і області":
        mode_two()
    else:
        logging.info("Робота завершена.")


if __name__ == "__main__":
    main()
