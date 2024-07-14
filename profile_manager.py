#! /usr/bin/env python
# -*- coding: utf-8 -*-

from botdriver import BotDriver
from os import path, stat
from pickle import load, dump
from os import system, name


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

    def edit_profile(self):
        while True:
            print("Выберите профиль для редактирования")
            print("x - вернуться в главное меню")
            for i, profile in enumerate(self.profiles):
                print(f"{i} - {profile['cat_name']}")
            answer = input("Выберите пункт: ")
            if answer.lower() == 'x':
                break
            try:
                index = int(answer)
                if 0 <= index < len(self.profiles):
                    profile = self.profiles[index]
                    print("Что вы хотите отредактировать?\n 1 - Имя\n2 - ID\n 3 - Почту\n4 - Пароль\n5 - Headless\n6 - User agent\n7 - Proxy\n0 - Отмена")

                    cmd = input("Выберите пункт: ")
                    system('cls' if name == 'nt' else 'clear')

                    if cmd == "1":
                        new_profile_name = input('Введите новое имя персонажа:')
                        profile['cat_name'] = new_profile_name
                        self.save_profiles()

                    elif cmd == "2":
                        new_profile_id = input('Введите новый айди персонажа:')
                        profile['cat_id'] = new_profile_id
                        self.save_profiles()

                    elif cmd == "3":
                        new_profile_login = input('Введите новую почту персонажа:')
                        profile['cat_login'] = new_profile_login
                        self.save_profiles()

                    elif cmd == "4":
                        new_profile_password = input('Введите новый пароль персонажа:')
                        profile['cat_password'] = new_profile_password
                        self.save_profiles()

                    elif cmd == "5":
                        new_profile_headless = input('Headless (True/False)?:')
                        profile['cat_is_headless'] = new_profile_headless.lower() == 'true'
                        self.save_profiles()

                    elif cmd == "6":
                        new_profile_ua = input('Введите новый user agent персонажа:')
                        profile['cat_user_agent'] = new_profile_ua
                        self.save_profiles()

                    elif cmd == "7":
                        new_profile_proxy = input('Введите новый прокси персонажа:')
                        profile['cat_proxy'] = new_profile_proxy
                        self.save_profiles()

                    elif cmd == "0":
                        break

                    else:
                        print("Не существующая команда")
                else:
                    print("Не существующая команда")
            except ValueError:
                print("Не существующая команда")

    def create_profile(self):
        cat_name = input("Введите имя персонажа:")
        cat_id = input("Введите айди персонажа:")
        cat_login = input("Введите почту для входа:")
        cat_password = input("Введите пароль для входа:")
        cat_is_headless = input("Headless (True/False):")
        cat_user_agent = input("Введите userAgent при необходимости. В противном случае - просто нажмите Enter.")
        cat_proxy = input("Введите адрес прокси сервера при необходимости. В противном случае - просто нажмите Enter.")

        cat_profile = {
                    'cat_name': cat_name,
                    'cat_id': cat_id,
                    'cat_login': cat_login,
                    'cat_password': cat_password,
                    'cat_is_headless': cat_is_headless.lower() == 'true',
                    'cat_user_agent': cat_user_agent,
                    'cat_proxy': cat_proxy
        }

        self.profiles.append(cat_profile)
        self.save_profiles()

    def delete_profile(self):
        profile_name_to_remove = input('Введите имя удаляемого персонажа:')
        for i, profile in enumerate(self.profiles):
            if profile["cat_name"] == profile_name_to_remove:
                self.profiles.pop(i)
                print(f"Профиль {profile_name_to_remove} успешно удалён")
                self.save_profiles()
                return 0

        print("Данного профиля не существует")

    def start_profile(self):
        while True:
            print("Выберите профиль для запуска.")
            print("x - вернуться в главное меню")
            for i, profile in enumerate(self.profiles):
                print(f"{i} - {profile['cat_name']}")
            answer = input("Выберите пункт: ")
            if answer.lower() == 'x':
                break
            try:
                index = int(answer)
                if 0 <= index < len(self.profiles):
                    profile = self.profiles[index]
                    bot = BotDriver(profile['cat_id'], profile['cat_login'], profile['cat_password'], profile['cat_is_headless'], profile['cat_user_agent'], profile['cat_proxy'])
                    bot.profile_initiate()

                else:
                    print("Не существующая команда")

            except ValueError:
                print("Не существующая команда")
