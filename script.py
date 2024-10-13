from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Zde zadej své přihlašovací údaje
USERNAME = 'thomasoffc12@gmail.com'  # Změň na svůj email
PASSWORD = 'Hakirama99@'  # Změň na své heslo

# Inicializace webového prohlížeče
driver = webdriver.Firefox()  # Pokud používáš Chrome, změň na webdriver.Chrome()

try:
    # Otevři webovou stránku Trading Analyzer
    driver.get('https://platform.tradinganalyzer.ai/login')

    # Čekání na načtení stránky
    time.sleep(3)  # Můžeš přizpůsobit podle potřeby

    # Najdi přihlašovací formulář a zadej své údaje
    username_field = driver.find_element(By.ID, 'email')  # ID pro email
    password_field = driver.find_element(By.ID, 'password')  # ID pro heslo

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Čekání na načtení hlavní stránky
    time.sleep(5)  # Můžeš přizpůsobit podle potřeby

    # Najdi a klikni na Score
    score_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Score')]")
    score_button.click()

    # Čekání na načtení dat po kliknutí na Score
    time.sleep(3)  # Můžeš přizpůsobit podle potřeby

    # Získání všech skóre
    # Vytvoříme XPath, který vyhledá všechny divy s textem skóre
    score_elements = driver.find_elements(By.XPATH, "//div[@class='flex h-14 flex-1 items-center justify-center px-2 py-3 text-center']")

    # Ulož skóre do souboru nebo je vypiš
    with open('forex_scores.txt', 'w') as file:
        for score in score_elements:
            file.write(score.text + '\n')
            print(score.text)

finally:
    driver.quit()  # Ukončí prohlížeč
