from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from random import uniform


class BotDriver:

    def __init__(self, char_id, char_login, char_password, is_headless=True, user_agent='', proxy=''):
        self.char_id = char_id
        self.char_login = char_login
        self.char_password = char_password
        self.is_headless = is_headless
        self.user_agent = user_agent
        self.proxy = proxy

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('detach', True)

        if is_headless:
            self.options.add_argument("--headless")

        if user_agent != '':
            self.options.add_argument(f"user-agent={self.user_agent}")

        if proxy != '':
            self.options.add_argument(f'--proxy-server={proxy}')

        self.driver = webdriver.Chrome(options=self.options)
        print(type(self.options.arguments), self.options.arguments)
        self.action = ActionChains(self.driver)

    def check_element_existance(self, element):
        try:
            self.driver.find_element(By.XPATH, element)
        except NoSuchElementException:
            return False
        return True

    def element_click(self, element):
        if self.check_element_existance(element):
            el = self.driver.find_element(By.XPATH, element)
            off_x = uniform(-(el.size['width']/2), el.size['width']/2)
            off_y = uniform(-(el.size['height']/2), el.size['height']/2)
            self.action.move_to_element_with_offset(el, int(off_x), int(off_y)).click().perform()

    def test_mouse(self):
        self.driver.get('https://keengo.ru/blog/javascript/opredelenie-koordinat-kursora-myshi/')
        sleep(3)
        self.element_click('/html/body/div[2]/div[1]/div[1]/div/h1')
        cords1 = self.driver.find_element(By.XPATH, '// *[ @ id = "coords1"]')
        print(cords1.text)
        self.driver.refresh()
        sleep(3)
        self.element_click('/html/body/div[2]/div[1]/div[1]/div/h1')
        cords2 = self.driver.find_element(By.XPATH, '// *[ @ id = "coords1"]')
        print(cords2.text)
        if cords1 == cords2:
            print("Оффсет не работает. Аварийное завершение работы программы.")
            self.driver.quit()

        else:
            print("Оффсет работает!")

    def botdriver_menu(self):
        self.test_mouse()
        self.safety_check()
        while True:
            print('Добро пожаловать на персонажа с ID ' + self.charID)
            print('0 - Вернуться в главное меню')
            print('1 - Перепроверка безопасности.')
            answer = input('Выберите действие:')
            if answer == '0':
                break
            elif answer == '1':
                self.test_mouse()
                self.safety_check()

    def safety_check(self):
        self.driver.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
        if self.check_element_existance("//*[@id='webdriver-result']") and self.driver.find_element(By.XPATH, "//*[@id='webdriver-result']").text == 'missing (passed)':
            print("Webdriver скрыт.")

            if self.check_element_existance("//*[@id='user-agent-result']") and self.driver.find_element(By.XPATH, "//*[@id='user-agent-result']").text == self.driver.execute_script("return navigator.userAgent;"):
                print('UserAgent валиден.')
                self.driver.quit()

        else:
            print("Webdriver не скрыт. Аварийное завершение работы программы.")
            self.driver.quit()

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state["charID"] = self.char_id
        state["charLogin"] = self.char_login
        state["charPassword"] = self.char_password
        state["isHeadless"] = self.is_headless
        state["userAgent"] = self.user_agent
        state["proxy"] = self.proxy
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.charID = state["charID"]
        self.charLogin = state["charLogin"]
        self.charPassword = state["charPassword"]
        self.isHeadless = state["isHeadless"]
        self.userAgent = state["userAgent"]
        self.proxy = state["proxy"]



