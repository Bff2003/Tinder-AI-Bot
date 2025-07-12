from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import selenium.webdriver.chrome.options
import os
import time
import dotenv
import selenium.webdriver.edge
import selenium.webdriver.edge.options
import selenium.webdriver.edge.service
import pickle
import random
import keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import json
from Utils import Utils
import os

dotenv.load_dotenv()

in_docker = os.getenv("IN_DOCKER", False)
if in_docker:
    # Configurações do Selenium
    selenium_url = os.getenv("http://tinder-ai-bot-selenium-1:4444", "http://tinder-ai-bot-selenium-1:4444/wd/hub")
    options = selenium.webdriver.edge.options.Options()
    # options.add_argument("--headless")  # Rodar sem interface gráfica
    options.add_argument("--no-sandbox")  # Necessário para Docker
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória no Docker
    options.add_argument("--disable-gpu")  # Recomendado para ARM e headless

    # Conectar ao WebDriver
    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=options
    )
else:
    options = selenium.webdriver.edge.options.Options()
    service = selenium.webdriver.edge.service.Service(executable_path="./msedgedriver.exe")
    driver = webdriver.Edge(service = service, options=options)

class TinderBot:

    def __init__(self, driver = None):
        self.driver = driver

    def login(self):
        self.driver.get("https://tinder.com/")
        # if cookie file exists, load cookies
        if os.path.exists("cookies.pkl"):
            with open("cookies.pkl", "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        else:
            # if cookie file doesn't exist, create it
            self.driver.get("https://tinder.com/")
            input("When you're logged in, press enter to continue...")
            cookies = self.driver.get_cookies()
            with open("cookies.pkl", "wb") as f:
                pickle.dump(cookies, f)
            print("Cookies saved to cookies.pkl")

    def get_profile_info(self):
        data = {}

        # Obrigatory info
        # profile pic: //*[@id="carousel-item-0"]/div
            # in style inside of background-image: url(&quot;

        # username: (//span[@itemprop='name'])[2]
        print("Extracting username...")
        username = Utils.wait_for_element(self.driver, "(//span[@itemprop='name'])[2]")
        if username is not None:
            print("Username:", username.text)
            username = username.text
            data["username"] = username

        # age: (//span[@itemprop='age'])[2]
        print("Extracting age...")
        age = Utils.wait_for_element(self.driver, "(//span[@itemprop='age'])[2]")
        if age is not None:
            print("Age:", age.text)
            age = age.text
            data["age"] = age

        # Click on button to see more info about profile
        button_open_profile = Utils.wait_for_element(self.driver, "(//div/button/*[local-name() = 'svg'])[4]")
        if button_open_profile is not None:
            button2 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button_open_profile))
            button2.click()

        # click in all "Ver todos" if exists
        # //*[contains(text(), 'Ver todos')]
        buttons_see_more = Utils.wait_for_elements(self.driver, "//*[contains(text(), 'Ver todos')]")
        print("Buttons see more:", buttons_see_more)
        
        # remove the last one (Fake Button) 
        buttons_see_more.pop()
        if buttons_see_more is not None and len(buttons_see_more) > 0:
            for button in buttons_see_more:
                # driver.implicitly_wait(10)
                # ActionChains(driver).move_to_element(button).click(button).perform()
                button2 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button))
                button2.click()

        relation_type = Utils.wait_for_element(self.driver, "((//h2[text()])/../..)[1]/div[2]")
        if relation_type is not None:
            print("Relation:", relation_type.text)
            relation_type = relation_type.text
            data["relation"] = relation_type

        # Sobre mim: //h2[text()='Sobre mim'], sobe 2, entra no 2
        about_me = Utils.wait_for_element(self.driver, "((//h2[text()='Sobre mim'])/../../div)[2]")
        if about_me is not None:
            print("About me:", about_me.text)
            about_me = about_me.text
            data["about_me"] = about_me

        # ((//h2[text()])/../..)/ul/li
        elements = Utils.wait_for_elements(self.driver, "((//h2[text()])/../..)/ul/li")
        if elements is not None:
            for element in elements:
                # get father of element
                element_father = element.find_element(By.XPATH, "../../div[1]")
                
                # if key dont exists 
                if element_father.text not in data:
                    data[element_father.text] = []
                
                # add element to list
                data[element_father.text].append(element.text)

        return data

    def click_pass_button(self):
        # (//div[contains(@class, 'gamepad-button-wrapper')])[3]
        button = Utils.wait_for_element(self.driver, "(//div[contains(@class, 'gamepad-button-wrapper')])[3]")
        Utils.click_button(button)

    def click_like_button(self):
        # (//div[contains(@class, 'gamepad-button-wrapper')])[5]
        button = Utils.wait_for_element(self.driver, "(//div[contains(@class, 'gamepad-button-wrapper')])[5]")
        Utils.click_button(button)

if __name__ == "__main__":
    try:
        tb = TinderBot(driver)
        tb.login()

        Utils.random_sleep(1, 3)

        USERS_PER_ROUND = 10
        ROUNDS = 1
        input("Press enter to START the bot...")

        input("Press enter to estract user info...")
        try:
            user = tb.get_profile_info()
            print(json.dumps(user, indent=4, ensure_ascii=False))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        

        input("Press enter to STOP the application...")
    finally:
        driver.quit()