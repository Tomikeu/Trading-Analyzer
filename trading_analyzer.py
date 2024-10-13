from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Načti své přihlašovací údaje z proměnných prostředí
USERNAME = os.getenv('USERNAME')  # Název proměnné prostředí pro uživatelské jméno
PASSWORD = os.getenv('PASSWORD')  # Název proměnné prostředí pro heslo

# Ověření, že uživatelské jméno a heslo jsou načteny
if USERNAME is None or PASSWORD is None:
    raise ValueError("Chybí přihlašovací údaje. Zkontroluj proměnné prostředí.")

# Inicializace webového prohlížeče v headless režimu
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Přidání headless režimu
driver = webdriver.Firefox(options=options)

try:
    # Otevři webovou stránku Trading Analyzer
    driver.get('https://platform.tradinganalyzer.ai/login')

    # Čekání na načtení stránky
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )

    # Najdi přihlašovací formulář a zadej své údaje
    username_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Čekání na načtení hlavní stránky
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Score')]"))
    )

    # Získání párů a jejich skóre
    pair_elements = driver.find_elements(By.XPATH, "//div[@class='flex h-14 items-center justify-center px-2 py-3 text-center flex-1 border-r border-gray-900']")
    score_elements = driver.find_elements(By.XPATH, "//div[@class='flex h-14 flex-1 items-center justify-center px-2 py-3 text-center']")

    # Ulož páry a skóre do souboru
    with open('forex_scores.txt', 'w') as file:
        for pair, score in zip(pair_elements, score_elements):
            file.write(f"{pair.text}: {score.text}\n")
            print(f"{pair.text}: {score.text}")

finally:
    driver.quit()  # Ukončí prohlížeč
