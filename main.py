import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import requests

# Funkce pro přihlašování a získání skóre
def get_score():
    # Nastavení možností Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Spuštění prohlížeče bez UI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Cesta k ovladači Chrome (uprav dle svého prostředí)
    service = Service(executable_path="/path/to/chromedriver")

    # Spuštění prohlížeče
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigace na přihlašovací stránku
        driver.get("https://trading-analyzer.com/login")
        
        # Čekání na načtení pole pro uživatelské jméno
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        username_input.send_keys(os.getenv("USERNAME"))

        # Najdi pole pro heslo a vyplň ho
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_input.send_keys(os.getenv("PASSWORD"))
        
        # Odešli formulář
        password_input.send_keys(Keys.RETURN)
        
        # Čekání na přesměrování a načtení stránky po přihlášení
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dashboard-element'))
        )

        # Získání skóre a symbolu (změň selektory podle potřeby)
        score_element = driver.find_element(By.CLASS_NAME, "score-class")
        symbol_element = driver.find_element(By.CLASS_NAME, "symbol-class")

        score = score_element.text
        symbol = symbol_element.text

        return symbol, score

    except Exception as e:
        print(f"Došlo k chybě: {e}")
    finally:
        driver.quit()

# Funkce pro aktualizaci Notion databáze
def update_notion(symbol, score):
    notion_api_url = f"https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_API_TOKEN')}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    data = {
        "parent": {"database_id": os.getenv('NOTION_DATABASE_ID')},
        "properties": {
            "Symbol": {"title": [{"text": {"content": symbol}}]},
            "Score": {"number": int(score)}
        }
    }

    response = requests.post(notion_api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Úspěšně aktualizováno v Notion.")
    else:
        print(f"Chyba při aktualizaci Notion: {response.status_code}, {response.text}")

# Funkce pro běh celého procesu
def run():
    symbol, score = get_score()
    if symbol and score:
        update_notion(symbol, score)

# Naplánuj spuštění každých X minut (nastav dle potřeby)
schedule.every(10).minutes.do(run)

# Nekonečný cyklus pro běh naplánovaných úloh
while True:
    schedule.run_pending()
    time.sleep(1)
