from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from random import randint, uniform, choice
from time import sleep
from tribes import tribes

home_page = 'https://catwar.su/'
game_page = 'https://catwar.su/cw3/'


class GameInterface:
    def __init__(self, driver):
        self.bot_driver = driver

    def get_my_profile(self):
        try:
            if self.bot_driver.driver.current_url != home_page:
                self.bot_driver.driver.get(home_page)
                sleep(3)

            my_name = self.bot_driver.driver.find_element(By.XPATH, '//*[@id="pr"]/big').text
            my_age = self.bot_driver.driver.find_element(By.XPATH, '//*[@id="pr"]/table/tbody/tr[2]/td[2]/b').text
            my_tribe = self.bot_driver.driver.find_element(By.XPATH, '//*[@id="pr"]/table/tbody/tr[3]/td[2]/b').text
            my_total_activity = self.bot_driver.driver.find_element(By.XPATH, '//*[@id="act_name"]').text
            self.bot_driver.element_click('//*[@id="act_icon"]')
            sleep(3)
            my_weekly_activity = self.bot_driver.driver.find_element(By.XPATH, '//*[@id="info"]/b').text

            my_profile = {
                "Имя": my_name,
                "Возраст": my_age,
                "Племя": my_tribe,
                "Активность": my_total_activity,
                "Недельная активность": my_weekly_activity
            }
            return my_profile

        except:
            print('Что-то пошло не так')
            self.bot_driver.driver.quit()

    @staticmethod
    def random_time():
        f1 = randint(1, 1000)
        if 1 <= f1 <= 700:
            return uniform(1.0, 10.0)
        elif 700 < f1 <= 900:
            return uniform(11.0, 30.0)
        elif 900 < f1 <= 960:
            return uniform(30.0, 90.0)
        elif 960 < f1 <= 1000:
            return uniform(90.0, 720.0)

    def get_current_action_timer(self):
        current_action_timer = self.bot_driver.driver.find_element(By.XPATH, '//*[@id="sek"]')
        while self.bot_driver.check_element_existance('//*[@id="sek"]'):
            print(f"Время действия: {current_action_timer.text}")
            sleep(10)
        print("Действие выполнено.")

    def way_click(self, way):
        off_x = uniform(-(way.size['width']/2), way.size['width']/2)
        off_y = uniform(-(way.size['height']/2), way.size['height']/2)
        self.bot_driver.action.move_to_element_with_offset(way, off_x, off_y).click().perform()
        sleep(3)

    def get_current_ways_list(self):
        sleep(3)
        ways_list = self.bot_driver.driver.find_elements(By.XPATH, '//*[@class="move_name"]')
        print("Доступные переходы:")
        for way in ways_list:
            print(f"{str(ways_list.index(way))} - {way.text}")
        return ways_list

    def get_my_current_location(self):
        sleep(3)
        my_current_location = self.bot_driver.driver.find_element(By.XPATH, '//*[@id="location"]').text
        return my_current_location

    def exception_leaving(self):
        print("Не вижу элементов игровой. Выполняю обновление страницы и пытаюсь возобновить работу.")
        self.bot_driver.driver.refresh()
        sleep(10)
        self.gain_activity()

    def gain_activity(self):
        try:
            allowed_locations = tribes[self.get_my_profile()["Племя"]]['allowed locations']
            while True:
                if self.bot_driver.driver.current_url != game_page:
                    self.bot_driver.driver.get(game_page)
                    sleep(3)
                random_delay = self.random_time()
                print(allowed_locations)
                print(random_delay)
                print(self.get_my_current_location())
                sleep(4)
                current_ways_list = self.get_current_ways_list()
                allowed_ways_on_current_location = []
                for way in current_ways_list:
                    if way.text in allowed_locations:
                        allowed_ways_on_current_location.append(way)
                selected_way = choice(allowed_ways_on_current_location)
                sleep(random_delay)
                print("Перехожу в", allowed_ways_on_current_location[allowed_ways_on_current_location.index(selected_way)].text)
                self.way_click(selected_way)
                sleep(1)
                self.get_current_action_timer()

        except NoSuchElementException:
            self.exception_leaving()
        except IndexError:
            self.exception_leaving()
        except ElementNotInteractableException:
            self.exception_leaving()
        except StaleElementReferenceException:
            self.exception_leaving()
