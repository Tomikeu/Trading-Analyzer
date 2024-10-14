import requests
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from notion_client import Client
import os

# Připojení k Notion
notion = Client(auth=os.getenv("NOTION_API_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

def get_score():
    # Selenium nastavení
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Spustí prohlížeč bez grafického rozhraní
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Spustí Chrome s webdriverem
    driver = webdriver.Chrome(options=chrome_options)
    
    # Navštíví stránku Trading Analyzer a přihlásí se
    driver.get('URL_TVÉ_TRADING_STRÁNKY')
    username_input = driver.find_element("name", "username")
    password_input = driver.find_element("name", "password")

    username_input.send_keys(os.getenv("USERNAME"))
    password_input.send_keys(os.getenv("PASSWORD"))
    driver.find_element("id", "login").click()

    # Extrahuje data
    symbol = "TEST_SYMBOL"
    score = 95  # Tady vlož skutečnou logiku pro zisk skóre

    driver.quit()
    return symbol, score

def update_notion(symbol, score):
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Symbol": {"title": [{"text": {"content": symbol}}]},
            "Score": {"number": score}
        }
    )

def run():
    symbol, score = get_score()
    update_notion(symbol, score)

# Naplánování spuštění každou hodinu
schedule.every().hour.do(run)

while True:
    schedule.run_pending()
