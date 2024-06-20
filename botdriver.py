from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from random import uniform


class botDriver():

    def __init__ (self, charID, charLogin, charPassword, isHeadless=True, userAgent='', proxy=''):
        self.charID = charID
        self.charLogin = charLogin
        self.charPassword = charPassword
        self.isHeadless = isHeadless
        self.userAgent = userAgent
        self.proxy = proxy


        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('detach', True)

        if (isHeadless):
            self.options.add_argument("--headless")

        if (userAgent != ''):
            self.options.add_argument("user-agent="+userAgent)

        if (proxy != ''):
            self.options.add_argument(f'--proxy-server={proxy}')

        self.driver = webdriver.Chrome(options=self.options)
        print(type(self.options.arguments), self.options.arguments)
        self.action = ActionChains(self.driver)


    def checkElementExistance(self, element):
        try:
            self.driver.find_element(By.XPATH, element)
        except NoSuchElementException:
            return False
        return True
    def elementClick(self, element):
        if self.checkElementExistance(element):
            el = self.driver.find_element(By.XPATH, element)
            offX = uniform(-(el.size['width']/2), el.size['width']/2)
            offY = uniform(-(el.size['height']/2), el.size['height']/2)
            self.action.move_to_element_with_offset(el, offX, offY).click().perform()


    def testMouse(self):
        self.driver.get('https://keengo.ru/blog/javascript/opredelenie-koordinat-kursora-myshi/')
        sleep(3)
        self.elementClick('/html/body/div[2]/div[1]/div[1]/div/h1')
        cords1 = self.driver.find_element(By.XPATH,'// *[ @ id = "coords1"]')
        print(cords1.text)
        self.driver.refresh()
        sleep(3)
        self.elementClick('/html/body/div[2]/div[1]/div[1]/div/h1')
        cords2 = self.driver.find_element(By.XPATH,'// *[ @ id = "coords1"]')
        print(cords2.text)
        if cords1 == cords2:
            print("Оффсет не работает. Аварийное завершение работы программы.")
            self.driver.quit()

        else:
            print("Оффсет работает!")


    def botDriverMenu(self):
        self.testMouse()
        self.safetyCheck()
        while True:
            print('Добро пожаловать на персонажа с ID '+ self.charID)
            print('0 - Вернуться в главное меню')
            print('1 - Перепроверка безопасности.')
            answer = input('Выберите действие:')
            if answer == '0':
                break
            elif answer == '1':
                self.testMouse()
                self.safetyCheck()
    def safetyCheck(self):
        self.driver.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
        if self.checkElementExistance("//*[@id='webdriver-result']") and self.driver.find_element(By.XPATH, "//*[@id='webdriver-result']").text == 'missing (passed)':
            print("Webdriver скрыт.")

            if self.checkElementExistance("//*[@id='user-agent-result']") and self.driver.find_element(By.XPATH, "//*[@id='user-agent-result']").text == self.driver.execute_script("return navigator.userAgent;"):
                print('UserAgent валиден.')
                self.driver.quit()

        else:
            print("Webdriver не скрыт. Аварийное завершение работы программы.")
            self.driver.quit()

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state["charID"] = self.charID
        state["charLogin"] = self.charLogin
        state["charPassword"] = self.charPassword
        state["isHeadless"] = self.isHeadless
        state["userAgent"] = self.userAgent
        state["proxy"] = self.proxy
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.charID = state["charID"]
        self.charLogin = state["charLogin"]
        self.charPassword = state["charPassword"]
        self.isHeadless = state["isHeadless"]
        self.userAgent = state["userAgent"]
        self.proxy = state["proxy"]



