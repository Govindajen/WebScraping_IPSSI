from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

import argparse
import csv
import os

""" def getDoctors (number, location, type, assurance_type, consultation_type, price_range): """
def getDoctors (type , location, max_results, visio = False):
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
        time.sleep(2)


        type_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "input.searchbar-input.searchbar-query-input")))

        type_input.clear()
        type_input.send_keys(type)
        time.sleep(2)
        type_input.send_keys(Keys.ENTER)
        

        wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
            "button.searchbar-submit-button")))
        
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button.searchbar-submit-button")))
        

        search_button.send_keys(Keys.ENTER)
        
        time.sleep(10)
        doctors = []

        cards = driver.find_elements(By.CSS_SELECTOR, "article.dl-p-doctor-result-card")
        for i in range(len(cards[:max_results])):
            try:
                
                card = driver.find_elements(By.CSS_SELECTOR, "article.dl-p-doctor-result-card")[i]
                h2_element = card.find_element(By.CSS_SELECTOR, "h2.dl-text.dl-text-body.dl-text-bold.dl-text-s.dl-text-primary-110")
                
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", h2_element)
                time.sleep(1)
                isVideoConsult = None
                try:
                    video_icon = card.find_element(By.CSS_SELECTOR, "div.dl-round-icon-placeholder svg[aria-label='Consultation vidéo disponible']")
                    if (video_icon):
                        isVideoConsult = True
                    isVideoConsult = True
                except: 
                    isVideoConsult = False

                # Wait for element to be clickable
                wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.dl-text.dl-text-body.dl-text-bold.dl-text-s.dl-text-primary-110"))
                )

                wait.until(EC.element_to_be_clickable(h2_element)).click()
                
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.dl-text.dl-text-bold.dl-text-title.dl-text-xl.dl-profile-header-name span[itemprop='name']")))

                name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.dl-text.dl-text-bold.dl-text-title.dl-text-xl.dl-profile-header-name span[itemprop='name']"))).text
                address = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.dl-profile-card-content div.dl-profile-text div"))).text
                
                if visio:
                    if isVideoConsult:
                        doctors.append({
                            "Name": name,
                            "Address": address,
                            "Consultation Type": "Visio"
                        })
                    else:
                        print(f"No video consultation available for {name}")
                else:
                    if not isVideoConsult:
                        doctors.append({
                            "Name": name,
                            "Address": address,
                            "Consultation Type": "In Person"
                        })
                    else:
                        print(f"Video consultation available for {name}")

                print("Name: ", name)
                print("address: ", address)

                driver.back()
            finally:
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.w-full")))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                if len(doctors) > 0:
                    
                    # Create filename with timestamp
                    filename = f"doctors.csv"
                    
                    # Write doctors data to CSV
                    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['Name', 'Address', 'Consultation Type']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        
                        writer.writeheader()
                        for doctor in doctors:
                            writer.writerow(doctor)
                    
                    print(f"CSV file created: {os.path.abspath(filename)}")


            

        print("Doctors: ", doctors)
        print('filtered doctors: ', len(doctors))
        print("Doctors found: ", len(cards))
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch doctors from Doctolib.")
    parser.add_argument("--type", required=True, help="Type of doctor (e.g., Médecin généraliste)")
    parser.add_argument("--location", required=True, help="Location (e.g., postal code or city)")
    parser.add_argument("--max_results", type=int, default=10, help="Maximum number of results to fetch")
    parser.add_argument("--visio", action="store_true", help="Include only video consultations")

    args = parser.parse_args()

    getDoctors(
        type=args.type,
        location=args.location,
        max_results=args.max_results,
        visio=args.visio
    )

    """ python doctlib_c_govin.py --type "generaliste" --location "78140" --max_results 5 --visio """
    """ python doctlib_c_govin.py --type "generaliste" --location "78140" --max_results 5 """