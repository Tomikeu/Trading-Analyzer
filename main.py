from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import schedule
import time

def get_score():
    # Nastavení prohlížeče Chrome (headless mód pro běh na serveru)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Běží bez zobrazení GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Inicializace WebDriveru
    driver = webdriver.Chrome(options=chrome_options)
    
    # Otevření stránky a přihlášení
    driver.get("https://www.tradinganalyzer.com")
    
    # Přihlášení na webovou stránku
    username_input = driver.find_element("name", "username")
    password_input = driver.find_element("name", "password")
    submit_button = driver.find_element("name", "submit")
    
    username_input.send_keys("tvůj_username")  # Tady použij environment proměnné
    password_input.send_keys("tvé_heslo")
    submit_button.click()

    # Extrahování výsledků
    symbol = driver.find_element("xpath", "tvůj_xpath_pro_symbol").text
    score = driver.find_element("xpath", "tvůj_xpath_pro_score").text
    
    driver.quit()
    return symbol, score

# Plánování úkolu
def run():
    symbol, score = get_score()
    print(f"Symbol: {symbol}, Score: {score}")

# Spuštění úkolu každých X minut
schedule.every(10).minutes.do(run)

# Běží neustále
while True:
    schedule.run_pending()
    time.sleep(1)
