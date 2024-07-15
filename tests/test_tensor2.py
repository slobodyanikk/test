import pytest
from selenium import webdriver
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_change_region(driver):
    # Шаг 1: Перейти на https://sbis.ru/ в раздел "Контакты"
    driver.get("https://sbis.ru/")
    sbis_page = SbisPage(driver)
    wait = WebDriverWait(driver, 10)

    sbis_page.go_to_contacts()
    wait.until(EC.visibility_of_element_located(sbis_page.region_label))

    # Шаг 2: Проверить текущий регион и список партнеров
    current_region = sbis_page.get_current_region()
    assert current_region == "Тюменская обл.", f"Ожидался регион 'Тюменская обл.', но получен {current_region}"
    assert sbis_page.get_partners_list(), "Список партнеров не найден"

    # Шаг 3: Изменить регион на "Камчатский край"
    sbis_page.change_region("Камчатский край")
    wait.until(EC.text_to_be_present_in_element(sbis_page.region_label, "Камчатский край"))

    # Шаг 4: Проверить, что регион изменился, список партнеров обновился, URL и заголовок изменились
    wait = WebDriverWait(driver, 10)
    new_region = sbis_page.get_current_region()
    wait = WebDriverWait(driver, 10)
    assert new_region == "Камчатский край", f"Ожидался регион 'Камчатский край', но получен {new_region}"
    assert sbis_page.get_partners_list(), "Список партнеров не обновился или не найден"
    assert sbis_page.check_partners_chenges(), "Список партнеров не обновился"

    current_url = driver.current_url
    assert "41-kamchatskij-kraj" in current_url, f"Ожидался URL с 'kamchatskiy-kray', но получен {current_url}"

    page_title = driver.title
    assert "Камчатский край" in page_title, f"Ожидался заголовок с 'Камчатский край', но получен {page_title}"
