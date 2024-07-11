from profile_manager import ProfileManager
from os import system, name


def main():
    profile_manager = ProfileManager()

    while True:
        print("Добро пожаловать в менеджер ботов!")

        print("1. Добавить профиль персонажа")
        print("2. Удалить профиль персонажа")
        print("3. Запустить персонажа через бота")
        print("0. Выход")

        cmd = input("Выберите пункт: ")
        system('cls' if name == 'nt' else 'clear')

        if cmd == "1":
            profile_manager.create_profile()
        elif cmd == "2":
            to_remove = input("Введите имя удаляемого персонажа:")
            profile_manager.delete_profile(to_remove)
        elif cmd == "3":
            profile_manager.start_profile()
        elif cmd == "0":
            break

        else:
            print("Не существующая команда")


if __name__ == "__main__":
    main()
