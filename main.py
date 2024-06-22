from botdriver import BotDriver
import os
import pickle


def start_profile(profile_list):
    while True:
        print("Выберите профиль для запуска.")
        print("x - вернуться в главное меню")
        for i in range(0, len(profile_list)):
            print(str(i)+" - "+profile_list[i]["Имя персонажа"])
        answer = input("Выберите пункт:")
        if answer == 'x':
            break
        elif profile_list[int(answer)] in profile_list:
            bot = BotDriver(profile_list[int(answer)]['driver'].charID, profile_list[int(answer)]['driver'].charLogin, profile_list[int(answer)]['driver'].charPassword, profile_list[int(answer)]['driver'].isHeadless, profile_list[int(answer)]['driver'].userAgent, profile_list[int(answer)]['driver'].proxy)
            bot.botdriver_menu()
        else:
            print("Не существующая команда")


def save_profile_list(profile_list):
    with open("profiles.pkl", "wb") as fp:
        pickle.dump(profile_list, fp)
    return 0


def delete_cat_profile(profile_list, name):
    for i in range(0, len(profile_list)):
        if profile_list[i]["Имя персонажа"] == name:
            profile_list.pop(i)
            print(f"Профиль {name} успешно удалён")
            break
    print("Данного профиля не существует")


def create_cat_profile(profile_list):
    cat_name = input("Введите имя персонажа:")
    cat_id = input("Введите айди персонажа:")
    cat_login = input("Введите почту для входа:")
    cat_password = input("Введите пароль для входа:")
    cat_is_headless = bool(input("Открыть ли окно, в котором работает бот? (True/False)"))
    cat_user_agent = input("Введите userAgent при необходимости. В противном случае - просто нажмите Enter.")
    cat_proxy = input("Введите адрес прокси сервера при необходимости. В противном случае - просто нажмите Enter.")

    cat_profile = {"Имя персонажа": cat_name, "driver": BotDriver(cat_id, cat_login, cat_password, cat_is_headless, cat_user_agent, cat_proxy)}
    return profile_list.append(cat_profile)


def main():
    profiles = []
    if os.stat("profiles.pkl").st_size > 0:
        with open('profiles.pkl', 'rb') as file:
            profiles = pickle.load(file)

    while True:
        print("Добро пожаловать в менеджер ботов!")

        print("1. Добавить профиль персонажа")
        print("2. Удалить профиль персонажа")
        print("3. Запустить персонажа через бота")
        print("0. Выход")

        cmd = input("Выберите пункт: ")

        if cmd == "1":
            os.system('cls')
            create_cat_profile(profiles)
            save_profile_list(profiles)
            os.system('cls')

        elif cmd == "2":
            os.system('cls')
            to_remove = input("Введите имя удаляемого персонажа:")
            delete_cat_profile(profiles, to_remove)
            save_profile_list(profiles)
            os.system('cls')

        elif cmd == "3":
            os.system('cls')
            start_profile(profiles)
            os.system('cls')

        elif cmd == "0":
            break
        else:
            print("Не существующая команда")


if __name__ == "__main__":
    main()
