from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


""" def getDoctors (number, location, type, assurance_type, consultation_type, price_range): """
def getDoctors (type , location):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 20)

    try: 
        driver.get("https://www.doctolib.fr/")

        try:
            refuseBtn = wait.until(
                EC.element_to_be_clickable((By.ID,
                    "didomi-notice-disagree-button")))
            
            refuseBtn.click()

            wait.until(EC.invisibility_of_element_located((By.ID,
                    "didomi-notice-disagree-button")))
        except:
            pass
            

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "input.searchbar-input.searchbar-query-input")))
        
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                "input.searchbar-input.searchbar-place-input")))
        
        location_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "input.searchbar-input.searchbar-place-input")))
        
        location_input.clear()
        location_input.send_keys(location)


        type_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "input.searchbar-input.searchbar-query-input")))

        type_input.clear()
        type_input.send_keys(type)

        wait.until(
            EC.text_to_be_present_in_element_value((By.CSS_SELECTOR,
                "input.searchbar-input.searchbar-query-input"),
            type))
        
        wait.until(
            EC.text_to_be_present_in_element_value((By.CSS_SELECTOR,
                "input.searchbar-input.searchbar-place-input"),
                location))

        location_input.send_keys(Keys.ENTER)
        
        time.sleep(10)
    finally:
        driver.quit()

getDoctors(
        type = "generaliste",
        location = "92330",
        )