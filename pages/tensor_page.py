from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class TensorPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.sila_v_lyudyah_block = (
            By.XPATH,
            '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div')
        self.more_link = (By.XPATH,
                          '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div/p[4]/a')
        self.about_url = "https://tensor.ru/about"
        self.timeline_photos = (By.CSS_SELECTOR, '.s-Grid-col .tensor_ru-About__block3-image')

    def check_sila_v_lyudyah_block(self):
        try:
            # повторные попытки для поиска блока
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.sila_v_lyudyah_block)
            )
            element = self.driver.find_element(*self.sila_v_lyudyah_block)
            return element.is_displayed()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Ошибка при поиске блока 'Сила в людях': {e}")
            return False

    def click_more_link(self):
        try:
            more_link_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.more_link)
            )
            # Прокрутка до элемента, чтобы убедиться, что он видим
            self.driver.execute_script("arguments[0].scrollIntoView(true);", more_link_element)
            more_link_element.click()
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("about")
            )
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
            print(f"Ошибка при клике по ссылке 'Подробнее': {e}")

    def verify_about_page(self):
        current_url = self.driver.current_url
        print(f"Текущий URL: {current_url}")
        return current_url.startswith(self.about_url)

    def get_timeline_photo_dimensions(self):
        photos = self.driver.find_elements(*self.timeline_photos)
        dimensions = [(photo.get_attribute('width'), photo.get_attribute('height')) for photo in photos]
        return dimensions
