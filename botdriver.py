from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from time import sleep
from random import uniform
from os import path
from pickle import dump, load
from game import GameInterface


class BotDriver:

    def __init__(self, char_id, char_login, char_password, is_headless, user_agent='', proxy=''):
        self.char_id = char_id
        self.char_login = char_login
        self.char_password = char_password
        self.is_headless = is_headless
        self.user_agent = user_agent
        self.proxy = proxy
        print('Headless:', type(is_headless), is_headless)

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('detach', True)

        if is_headless:
            self.options.add_argument("--headless")

        if user_agent != '':
            self.options.add_argument(f"user-agent={self.user_agent}")

        if proxy != '':
            proxy_url = f"http://{self.proxy}"
            selenium_wire_options = {
                "proxy": {
                    "http": proxy_url,
                    "https": proxy_url
                },
                'backend': 'mitmproxy',
                'ignore_http_methods': ['CONNECT']
            }
            self.driver = webdriver.Chrome(options=self.options, seleniumwire_options=selenium_wire_options)
            self.action = ActionChains(self.driver)

        else:
            self.driver = webdriver.Chrome(options=self.options)
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


    def profile_initiate(self):
        self.safety_check()

        self.cw_auto()

        game_interface = GameInterface(self)
        game_interface.gain_activity()

        self.driver.quit()

    def safety_check(self):
        self.driver.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
        if self.check_element_existance("//*[@id='webdriver-result']") and self.driver.find_element(By.XPATH, "//*[@id='webdriver-result']").text == 'missing (passed)':
            print("Webdriver скрыт.")

            if self.check_element_existance("//*[@id='user-agent-result']") and self.driver.find_element(By.XPATH, "//*[@id='user-agent-result']").text == self.user_agent:
                print('UserAgent валиден.')
                print(f'UserAgent:{self.driver.find_element(By.XPATH, "//*[@id='user-agent-result']").text}')
                self.driver.get('https://2ip.ru/')

                sleep(3)

                ip = self.driver.find_element(By.XPATH, "//*[@id='d_clip_button']/span").text
                print("IP:" + ip)
                if self.proxy != '' and ip not in self.proxy:
                    print('Прокси не скрыл айпи. Принудительный выход.')
                    self.driver.quit()

            else:
                print("Не валидный UserAgent. Принудительный выход.")
                self.driver.quit()


        else:
            print("Webdriver не скрыт. Принудительный выход.")
            self.driver.quit()

    def cw_auto(self):
        print("Проверка cookie...")
        cookie_exist = path.exists(f"cookies/{self.char_id}_cookie")
        self.driver.get('https://catwar.su/login')
        if cookie_exist:
            print("Обнаружен файл cookie. Начинаем загрузку...")
            for cookie in load(open(f"cookies/{self.char_id}_cookie", "rb")):
                self.driver.add_cookie(cookie)
            sleep(3)
            self.driver.get('https://catwar.su')
            sleep(3)
            if self.check_element_existance('//*[@id="emblem"]'):
                print("Cookie успешно загружены. Вход завершен.")

        else:
            print("Cookie не обнаружены. Выполняется аутентификация.")
            sleep(3)
            login = self.char_login
            password = self.char_password

            mail_input = self.driver.find_element(By.ID, 'mail')
            mail_input.send_keys(login)

            password_input = self.driver.find_element(By.ID, 'pass')
            password_input.send_keys(password)

            self.element_click('//*[@id="form"]/input[2]')
            sleep(3)
            if self.check_element_existance('//*[@id="emblem"]'):
                print("Авторизация завершена. Сохраняем куки.")
                dump(self.driver.get_cookies(), open(f"cookies/{self.char_id}_cookie", "wb"))
        sleep(3)

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {"char_id": self.char_id, "char_login": self.char_login, "char_password": self.char_password,
                 "is_headless": self.is_headless, "user_agent": self.user_agent, "proxy": self.proxy}
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.char_id = state["char_id"]
        self.char_login = state["char_login"]
        self.char_password = state["char_password"]
        self.is_headless = state["is_headless"]
        self.user_agent = state["user_agent"]
        self.proxy = state["proxy"]
