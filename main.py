from botdriver import botDriver
import os
import pickle

def startProfile(profileList):
    while True:
        print("Выберите профиль для запуска.")
        print("x - вернуться в главное меню")
        for i in range (0, len(profileList)):
            print(str(i)+" - "+profileList[i]["Имя персонажа"])
        answer = input("Выберите пункт:")
        if answer == 'x':
            break
        elif profileList[int(answer)] in profileList:
            bot = botDriver(profileList[int(answer)]['driver'].charID, profileList[int(answer)]['driver'].charLogin, profileList[int(answer)]['driver'].charPassword, profileList[int(answer)]['driver'].isHeadless, profileList[int(answer)]['driver'].userAgent, profileList[int(answer)]['driver'].proxy)
            bot.botDriverMenu()
        else:
            print("Не существующая команда")
def saveProfileList(profileList):
    with open("profiles.pkl", "wb") as fp:
        pickle.dump(profileList, fp)
    return 0
def deleteCatProfile(profileList, name):
    for i in range(0, len(profileList)):
        if profileList[i]["Имя персонажа"] == name:
            profileList.pop(i)
            print("Профиль " + name + " успешно удалён")
            break
    print("Данного профиля не существует")


def createCatProfile(profileList):
    catName = input("Введите имя персонажа:")
    catId = input ("Введите айди персонажа:")
    catLogin = input ("Введите почту для входа:")
    catPassword = input ("Введите пароль для входа:")
    catIsHeadless = bool(input ("Открыть ли окно, в котором работает бот? (True/False)"))
    catUA = input ("Введите userAgent при необходимости. В противном случае - просто нажмите Enter.")
    catProxy = input ("Введите адрес прокси сервера при необходимости. В противном случае - просто нажмите Enter.")

    catProfile = {"Имя персонажа": catName, "driver": botDriver(catId, catLogin, catPassword, catIsHeadless, catUA, catProxy)}
    return profileList.append(catProfile)

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
            createCatProfile(profiles)
            saveProfileList(profiles)
            os.system('cls')



        elif cmd == "2":
            os.system('cls')
            toRemove = input("Введите имя удаляемого персонажа:")
            deleteCatProfile(profiles, toRemove)
            saveProfileList(profiles)
            os.system('cls')

        elif cmd == "3":
            os.system('cls')
            startProfile(profiles)
            os.system('cls')

        elif cmd == "0":
            break
        else:
            print("Не существующая команда")


if __name__ == "__main__":
    main()