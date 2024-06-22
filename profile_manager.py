from botdriver import BotDriver
from os import path, stat
from pickle import load, dump


class ProfileManager:
    def __init__(self, profile_file="profiles.pkl"):
        self.profile_file = profile_file
        self.profiles = self.load_profiles()

    def load_profiles(self):
        if path.exists(self.profile_file) and stat(self.profile_file).st_size > 0:
            with open(self.profile_file, 'rb') as file:
                return load(file)
        return []

    def save_profiles(self):
        with open(self.profile_file, "wb") as fp:
            dump(self.profiles, fp)
        return 0

    def create_profile(self):
        cat_name = input("Введите имя персонажа:")
        cat_id = input("Введите айди персонажа:")
        cat_login = input("Введите почту для входа:")
        cat_password = input("Введите пароль для входа:")
        cat_is_headless = input("Headless (True/False):")
        cat_user_agent = input("Введите userAgent при необходимости. В противном случае - просто нажмите Enter.")
        cat_proxy = input("Введите адрес прокси сервера при необходимости. В противном случае - просто нажмите Enter.")

        cat_profile = {
                    'сat_name': cat_name,
                    'cat_id': cat_id,
                    'cat_login': cat_login,
                    'cat_password': cat_password,
                    'cat_is_headless': cat_is_headless.lower() == 'true',
                    'cat_user_agent': cat_user_agent,
                    'cat_proxy': cat_proxy
        }

        self.profiles.append(cat_profile)
        self.save_profiles()

    def delete_profile(self, name):
        for i, profile in enumerate(self.profiles):
            if profile["cat_name"] == name:
                self.profiles.pop(i)
                print(f"Профиль {name} успешно удалён")
                self.save_profiles()
                return
        print("Данного профиля не существует")

    def start_profile(self):
        while True:
            print("Выберите профиль для запуска.")
            print("x - вернуться в главное меню")
            for i, profile in enumerate(self.profiles):
                print(f"{i} - {profile}")
            answer = input("Выберите пункт: ")
            if answer.lower() == 'x':
                break
            try:
                index = int(answer)
                if 0 <= index < len(self.profiles):
                    profile = self.profiles[index]
                    bot = BotDriver(profile['cat_id'], profile['cat_login'], profile['cat_password'], profile['cat_is_headless'], profile['cat_user_agent'], profile['cat_proxy'])
                    bot.botdriver_menu()
                else:
                    print("Не существующая команда")
            except ValueError:
                print("Не существующая команда")
