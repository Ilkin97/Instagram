import time
import random
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

# .env dosyasından bilgileri okuyun
SIMILAR_ACCOUNT = os.getenv("ACCOUNT")
USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")

# Loglama ayarları
logging.basicConfig(filename="bot.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def random_wait(min_wait=2, max_wait=5):
    """Rastgele bekleme süresi ekler."""
    time.sleep(random.uniform(min_wait, max_wait))

class InstaFollower:
    def __init__(self):
        self.driver = None
        self.start_browser()

    def start_browser(self):
        """Tarayıcıyı başlatır ve ayarlarını yapar."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlat
        chrome_options.add_argument("--disable-notifications")  # Bildirimleri devre dışı bırak
        chrome_options.add_argument("--disable-extensions")  # Eklentileri devre dışı bırak
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bot algılamayı önle
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Otomasyon bayrağını kaldır
        chrome_options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # WebDriver bayrağını gizle

    def restart_browser(self):
        """Tarayıcıyı yeniden başlatır."""
        logging.info("Tarayıcı yeniden başlatılıyor...")
        self.driver.quit()
        time.sleep(3)
        self.start_browser()

    def login(self):
        """Instagram'a giriş yapar."""
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            username_field = self.driver.find_element(By.NAME, 'username')
            password_field = self.driver.find_element(By.NAME, 'password')

            # Kullanıcı adı ve şifreyi yavaşça yaz
            self.slow_type(username_field, USERNAME)
            self.slow_type(password_field, PASSWORD)

            login_button = self.driver.find_element(
                By.XPATH, '//button[@type="submit"]'
            )
            login_button.click()

            # Giriş yapıldıktan sonra Instagram ana sayfasının yüklendiğini doğrulayın
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Home"]'))
            )
            logging.info("Giriş başarılı.")
        except TimeoutException as e:
            logging.error(f"Giriş sırasında zaman aşımı hatası: {e}")
            self.restart_browser()
            self.login()
        except WebDriverException as e:
            logging.error(f"Giriş sırasında WebDriver hatası: {e}")
            self.restart_browser()
            self.login()

    def slow_type(self, element, text):
        """Metni yavaşça yazar."""
        for character in text:
            element.send_keys(character)
            time.sleep(random.uniform(0.1, 0.3))  # Her karakter arasında rastgele bekleme

    def find_followers(self):
        """Belirli bir hesabın takipçilerini bulur ve takip eder."""
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

            num_followers_to_add = random.randint(100, 200)  # Daha küçük bir aralık seçildi
            followed_count = 0

            while followed_count < num_followers_to_add:
                random_wait(1, 3)  # Daha insana benzer davranışlar için kısa beklemeler ekleyin
                follow_buttons = self.driver.find_elements(
                    By.XPATH, '//button[text()="Follow"]'
                )

                for button in follow_buttons:
                    if followed_count >= num_followers_to_add:
                        break
                    try:
                        self.human_like_click(button)  # İnsan benzeri tıklama
                        followed_count += 1
                        logging.info(f"Takip edilen kullanıcı sayısı: {followed_count}")
                        random_wait(5, 10)  # Her takipten sonra daha uzun rastgele bekleme süresi
                    except ElementClickInterceptedException:
                        cancel_button = self.driver.find_element(
                            By.XPATH, '//button[text()="Cancel"]'
                        )
                        cancel_button.click()
        except WebDriverException as e:
            logging.error(f"Takipçi bulma sırasında hata: {e}")
            self.restart_browser()
            self.login()
            self.find_followers()

    def human_like_click(self, element):
        """İnsan benzeri tıklama işlemi."""
        actions = ActionChains(self.driver)
        actions.move_to_element(element).pause(random.uniform(0.5, 1.5)).click().perform()

    def logout(self):
        """Instagram'dan çıkış yapar."""
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
            logging.info("Çıkış başarılı.")
        except WebDriverException as e:
            logging.error(f"Çıkış sırasında hata: {e}")
            self.restart_browser()
            self.login()
            self.logout()

# Botu çalıştırmak için
if __name__ == "__main__":
    if not all([SIMILAR_ACCOUNT, USERNAME, PASSWORD]):
        logging.error(".env dosyasında eksik bilgi var!")
    else:
        bot = InstaFollower()
        bot.login()
        bot.find_followers()  # Takipçi ekleme işlemini başlat
        bot.logout()  # Çıkış yap
