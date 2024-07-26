from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def download(url):
    driver = webdriver.Chrome()

    try:
        driver.maximize_window()
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 400)")


        # Wait for the element to be clickable
        checkall = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "master-games-check-all")))
        checkall.click()


        if checkall.is_selected():
            print("Checkbox is clicked")
        else:
            print("Checkbox is not clicked")


        download_button = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.CLASS_NAME, "master-games-download-button")))
        download_button.click()

        time.sleep(3)

        driver.quit()
    except Exception as e:
        print("An error occurred:", e)


url = "https://www.chess.com/games/search?opening=&openingId=&p1=Magnus%20Carlsen&p2=Hikaru%20Nakamura&sort=8"

download(url)

time.sleep(10)

for pagenumber in range(2,12):
    newurl = url + "&page=" + str(pagenumber)
    download(newurl)
    time.sleep(10)


