import time
import random
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Service sınıfını içeri aktar
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

SIMILAR_ACCOUNT = os.getenv("ACCOUNT")  # .env dosyasından benzer hesabı okuyun
USERNAME = os.getenv("INSTA_USERNAME")  # .env dosyasından kullanıcı adını okuyun
PASSWORD = os.getenv("INSTA_PASSWORD")  # .env dosyasından şifreyi okuyun

logging.basicConfig(filename="bot.log", level=logging.INFO)

def random_wait(min_wait=2, max_wait=5):
    time.sleep(random.uniform(min_wait, max_wait))

class InstaFollower:
    def __init__(self):
        self.driver = None
        self.start_browser()

    def start_browser(self):
        # Chrome tarayıcısını başlatma
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat
        # chrome_options.add_argument('--headless')  # Headless modda çalıştırmak için açın
        
        # Service kullanarak tarayıcıyı başlatma
        service = Service(executable_path="C:/chromedriver/chromedriver.exe")  # ChromeDriver yolu
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def restart_browser(self):
        logging.info("Restarting browser...")
        self.driver.quit()
        time.sleep(3)
        self.start_browser()

    def login(self):
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            # Giriş için zaten profil kullanıyoruz, buna gerek yok
            logging.info("Login successful with existing session")
        except TimeoutException as e:
            logging.error(f"Login failed due to timeout: {e}")
            self.restart_browser()  # Yeniden başlat ve tekrar giriş yap
            self.login()
        except WebDriverException as e:
            logging.error(f"Login failed due to WebDriver error: {e}")
            self.restart_browser()  # Tarayıcıyı yeniden başlat ve tekrar giriş yap
            self.login()

    def find_followers(self):
        try:
            self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
            followers_link = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[contains(@href,"/followers/")]')
                )
            )
            followers_link.click()

            followers_popup = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]'))
            )

            num_followers_to_add = random.randint(1000, 5000)
            followed_count = 0
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while followed_count < num_followers_to_add:
                # Sayfa kaydırma ve yeni takipçi butonlarını yükleme
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
                random_wait(2, 5)  # Sayfa kaydırma işlemi sonrasında bekleme

                follow_buttons = self.driver.find_elements(
                    By.XPATH, '//button[text()="Follow"]'
                )

                for button in follow_buttons:
                    if followed_count >= num_followers_to_add:
                        break
                    try:
                        button.click()
                        followed_count += 1
                        random_wait(2, 5)  # Her takipten sonra rastgele bekleme süresi ekleyin
                    except ElementClickInterceptedException:
                        cancel_button = self.driver.find_element(
                            By.XPATH, '//button[text()="Cancel"]'
                        )
                        cancel_button.click()

                # Sayfa kaydırma için daha fazla öğe yüklendiğinde bekleme
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:  # Sayfa kaydırma sonrasında yeni öğe yüklenmezse çık
                    break
                last_height = new_height
        except WebDriverException as e:
            logging.error(f"Finding followers failed: {e}")
            self.restart_browser()
            self.login()
            self.find_followers()

    def logout(self):
        try:
            self.driver.get("https://www.instagram.com/")
            profile_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//span[@aria-label="Profile"]'))
            )
            profile_button.click()
            logout_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Log Out"]'))
            )
            logout_button.click()
        except WebDriverException as e:
            logging.error(f"Logout failed: {e}")
            self.restart_browser()
            self.login()
            self.logout()

# Botu çalıştırmak için
if __name__ == "__main__":
    bot = InstaFollower()
    bot.login()  # Mevcut oturumla giriş yap
    bot.find_followers()  # Takipçi ekleme işlemini başlat
    bot.logout()  # Çıkış yap
