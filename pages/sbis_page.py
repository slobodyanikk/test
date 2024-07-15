from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

old_partner_list = []


class SbisPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.contacts_link = (By.LINK_TEXT, 'Контакты')
        self.tensor_banner = (By.XPATH,
                              '//*[@id="contacts_clients"]/div[1]/div/div/div[2]/div/a')
        self.region_label = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text.sbis_ru-link")
        self.partner_list = (By.XPATH,
                             '//*[@id="contacts_list"]/div/div[2]/div[2]')
        self.region_option_by_title_template = '//li[contains(@class, "sbis_ru-Region-Panel__item")]/span[@title="{}"]'  # Поиск по title

    def go_to_contacts(self):
        self.driver.find_element(*self.contacts_link).click()

    def click_tensor_banner(self):
        try:
            # Повторное нахождение элемента перед кликом
            tensor_banner = self.wait.until(EC.element_to_be_clickable(self.tensor_banner))
            tensor_banner.click()
        except StaleElementReferenceException:
            # Повторная попытка нахождения элемента и клика
            tensor_banner = self.wait.until(EC.element_to_be_clickable(self.tensor_banner))
            tensor_banner.click()

    def get_current_region(self):
        return self.driver.find_element(*self.region_label).text

    def get_partners_list(self):
        old_partner_list = self.driver.find_elements(*self.partner_list)
        return len(self.driver.find_elements(*self.partner_list)) > 0

    def change_region(self, region_name):
        self.driver.find_element(*self.region_label).click()

        # XPath с title региона
        region_xpath = self.region_option_by_title_template.format(region_name)
        region_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, region_xpath))
        )
        region_element.click()

    def check_partners_chenges(self):
        return self.driver.find_elements(*self.partner_list) != old_partner_list

    def go_to_local_versions(self):
        footer = self.driver.find_element(*self.footer)
        local_versions_link = footer.find_element(*self.local_versions_link)
        ActionChains(self.driver).move_to_element(local_versions_link).perform()
        local_versions_link.click()
