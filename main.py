from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import dotenv

dotenv.load_dotenv()

# Configurações do Selenium
selenium_url = os.getenv("SELENIUM_URL", "http://tinder-ai-bot-selenium-1:4444/wd/hub")
options = Options()
# options.add_argument("--headless")  # Rodar sem interface gráfica
options.add_argument("--no-sandbox")  # Necessário para Docker
options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória no Docker
options.add_argument("--disable-gpu")  # Recomendado para ARM e headless

# Conectar ao WebDriver
driver = webdriver.Remote(
    command_executor=selenium_url,
    options=options
)

try:
    # Exemplo: acessar um site
    driver.get("https://www.google.com")
    print("Título da página:", driver.title)

    print("Sleeping for 20 seconds...")
    time.sleep(20)
    print("Done!")
finally:
    driver.quit()