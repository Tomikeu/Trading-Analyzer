import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import schedule

# Konfigurace pro Notion
NOTION_DATABASE_ID = '11639f192ac980c58282ec2d164ded5b'
NOTION_API_TOKEN = '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'
NOTION_API_URL = f'https://api.notion.com/v1/pages'

# Přihlašovací údaje pro Trading Analyzer
TRADING_ANALYZER_URL = 'https://platform.tradinganalyzer.ai/login'
USERNAME = 'thomasoffc12@gmail.com'
PASSWORD = 'Hakirama99@'

# Funkce pro přihlášení a získání score
def get_score():
    # Inicializace prohlížeče
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Pro tichý režim bez GUI
    driver = webdriver.Chrome(options=options)

    try:
        # Přihlášení k Trading Analyzer
        driver.get(TRADING_ANALYZER_URL)
        time.sleep(2)  # Čekání na načtení stránky

        # Najdi a vyplň přihlašovací údaje
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Čekání na přihlášení

        # Navigace na hlavní stránku
        driver.get('https://platform.tradinganalyzer.ai/')
        time.sleep(5)  # Čekání na načtení dat

        # Najdi symbol a score
        symbol = driver.find_element(By.XPATH, '//div[contains(text(),"AUD-NZD")]')
        score = symbol.find_element(By.XPATH, 'following-sibling::div')

        # Vytáhnout texty
        symbol_text = symbol.text
        score_text = score.text
        
        return symbol_text, score_text

    finally:
        driver.quit()

# Funkce pro aktualizaci dat v Notion
def update_notion(symbol, score):
    headers = {
        'Authorization': f'Bearer {NOTION_API_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    
    data = {
        'parent': { 'database_id': NOTION_DATABASE_ID },
        'properties': {
            'Symbol': { 'title': [{ 'text': { 'content': symbol } }] },
            'Score': { 'number': int(score) }
        }
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        print('Úspěšně aktualizováno v Notion')
    else:
        print('Chyba při aktualizaci v Notion:', response.text)

# Funkce pro spuštění
def run():
    symbol, score = get_score()
    update_notion(symbol, score)

# Naplánování úlohy, která běží každou hodinu
schedule.every(1).hours.do(run)

# Hlavní smyčka
while True:
    schedule.run_pending()
    time.sleep(1)
