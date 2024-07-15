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


def test_tensor_navigation(driver):
    # Шаг 1: Перейти на https://sbis.ru/ в раздел "Контакты"
    driver.get("https://sbis.ru/")
    sbis_page = SbisPage(driver)
    wait = WebDriverWait(driver, 10)
    sbis_page.go_to_contacts()

    # Шаг 2: Найти баннер Тензор, кликнуть по нему
    try:
        tensor_banner = wait.until(EC.element_to_be_clickable(sbis_page.tensor_banner))
        tensor_banner.click()
    except StaleElementReferenceException:
        tensor_banner = wait.until(EC.element_to_be_clickable(sbis_page.tensor_banner))
        tensor_banner.click()

    # Шаг 3: Перейти на https://tensor.ru/
    driver.switch_to.window(driver.window_handles[1])

    tensor_page = TensorPage(driver)
    # Шаг 4: Проверить, что есть блок "Сила в людях"
    assert tensor_page.check_sila_v_lyudyah_block()

    # Шаг 5: Перейдите в этом блоке в "Подробнее" и убедитесь, что открывается
    # https://tensor.ru/about
    tensor_page.click_more_link()

    # Ждем, пока текущий URL станет https://tensor.ru/about
    WebDriverWait(driver, 10).until(
        EC.url_contains(tensor_page.about_url)
    )

    # Проверяем, что URL содержит нужную подстроку
    assert tensor_page.verify_about_page(), f"Ожидался URL '{tensor_page.about_url}', но текущий URL: {driver.current_url}"

    # Шаг 6: Находим раздел Работаем и проверяем, что у всех фотографии хронологии
    # одинаковые высота (height) и ширина (width)
    dimensions = tensor_page.get_timeline_photo_dimensions()
    widths, heights = zip(*dimensions)

    # Преобразуем строки в числа для проверки
    widths = list(map(int, widths))
    heights = list(map(int, heights))

    # Проверка, что все ширины и высоты одинаковы
    assert len(set(widths)) == 1
    assert len(set(heights)) == 1
