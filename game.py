from selenium.webdriver.common.by import By
from time import sleep

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
                "Имя:": my_name,
                "Возраст:": my_age,
                "Племя:": my_tribe,
                "Активность:":my_total_activity,
                "Недельная активность:":my_weekly_activity
            }
            return my_profile

        except:
            print('Что-то пошло не так')
            self.bot_driver.driver.quit()



