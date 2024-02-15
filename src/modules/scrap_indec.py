import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os
import time


def inicio_driver(link:str):
    service = Service(ChromeDriverManager().install())
    carpeta_descarga=os.getcwd()+"\downloads"
    prefs = {'download.default_directory' : carpeta_descarga,
        "directory_upgrade": True}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(link)
    driver.maximize_window()
    return driver
    
def every_downloads_chrome():
    '''Check if all downloads are complete'''
    while True:
        carpeta_descarga=os.getcwd()+"\downloads"
        incomplete_downloads = [name for name in os.listdir(carpeta_descarga) if name.endswith('.tmp') or name.endswith('.crdownload')]
        if not incomplete_downloads:
            return True  # Return True when no more .crdownload files in the directory
        time.sleep(1)  # Wait for 1 second before checking again

def wait_for_downloads_to_complete(timeout:int):
    '''Wait for all downloads to complete with a timeout'''
    start_time = time.time()  # Save the start time

    while not every_downloads_chrome():  # Wait until all downloads are complete
        if time.time() - start_time > timeout:  # If the timeout has elapsed, break the loop
            print('Timeout elapsed, stopping downloads')
            break
        time.sleep(1)  # Wait for 1 second before checking again
            
    
    
def get_ica_digital_href(driver, timeout:int = 10):
    wait = WebDriverWait(driver, timeout)

    # Define the expected condition to wait for
    expected_condition = EC.presence_of_all_elements_located((By.XPATH, "//a[@class='btn btn-outline-success w-100 btn-sm max-w']"))

    # Wait for the elements to be loaded
    href_elements = wait.until(expected_condition)

    elements = driver.find_elements(By.XPATH, "//a[@class='btn btn-outline-success w-100 btn-sm max-w']")
    hrefs = [element.get_attribute('href') for element in elements]
    link_ica_digital = [href for href in hrefs if "ica_digital" in href][0]
    return link_ica_digital

def get_excels_from_ica_digital(driver, timeout:int=10):
    wait = WebDriverWait(driver, timeout)
    expected_condition = EC.presence_of_all_elements_located((By.XPATH, '//*[@id="graficoSaldo"]/astro-island/div/div/div'))
    href_elements = wait.until(expected_condition)
    elements = driver.find_elements(By.XPATH, "//a[@class]")
    hrefs = [element.get_attribute('href') for element in elements]
    excels = [excel for excel in hrefs if excel.endswith(".xlsx")]
    return excels

# def download_every_excel(driver,excels:list[str]):
#     for excel in excels:
#         driver.get(excel)
#     paths = WebDriverWait(driver, 300, 1).until(every_downloads_chrome)

def scrap_excels_index_ica_digital(timeout:int = 10):
    driver = inicio_driver("https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-2-40")
    link_ica_digital = get_ica_digital_href(driver,timeout)
    driver.get(link_ica_digital)
    excels = get_excels_from_ica_digital(driver)
    # download_every_excel(driver, excels)
    for excel in excels:
        driver.get(excel)
    wait_for_downloads_to_complete(timeout=300)
    driver.quit()
    