from profile_manager import ProfileManager
from os import system, name


def main():
    profile_manager = ProfileManager()

    while True:

        print("CWbot v. 2.0\n1 - Добавить профиль персонажа\n2 - Редактировать профиль персонажа\n3 - Удалить профиль персонажа\n4 - Запуск\nx - Выход")

        cmd = input("Выберите пункт: ")
        system('cls' if name == 'nt' else 'clear')

        if cmd == "1":
            profile_manager.create_profile()
        elif cmd == '2':
            profile_manager.edit_profile()
        elif cmd == "3":
            profile_manager.delete_profile()
        elif cmd == "4":
            profile_manager.start_profile()

        elif cmd == "x":
            break

        else:
            print("Не существующая команда")


if __name__ == "__main__":
    main()
