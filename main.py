import questionary
import emoji


def mode_one():
    print(f"{emoji.emojize(':hammer_and_wrench:')} Обрано режим 1: Створення звіту на основі всіх файлів.")


def mode_two():
    print(f"{emoji.emojize(':bar_chart:')} Обрано режим 2: Створення звіту по даті і області.")
    setting1 = input("Введіть області які вас цікавлять через кому (приклад: Київська, Херсонська, Вінницька): ")
    setting2 = input("Введіть місяць та рік на основі яких формувати звіт в форматі 01_2025-05_2025: ")
    print(f"Режим 2: налаштування1={setting1}, налаштування2={setting2}")



def main():
    greeting = [
        f"{emoji.emojize(':police_officer:')} Привіт, це скрипт який допомагає зформувати статистику затримань по всій Україні.",
        f"{emoji.emojize(':classical_building:')} Розроблений для Департаменту головної інспекції та дотримання прав людини."
    ]
    print(greeting[0])
    print(greeting[1])

    choice = questionary.select(
        "Оберіть режим роботи скрипта:",
        choices=[
            "Створення звіту на основі всіх файлів",
            "Створення звіту по даті і області",
        ]).ask()

    if choice == "Звіт на основі всіх файлів":
        mode_one()
    elif choice == "Звіт по даті та області":
        mode_two()
    else:
        print("Помилка.")


if __name__ == "__main__":
    main()
