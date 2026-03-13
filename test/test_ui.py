import os
import sys
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import (
    BASE_URL_UI, MOVIE_TITLE, MOVIE_STR_UI, MOVIE_URL, SEARCH_QUERY
)

# Исправление E402: импорты из config перенесены выше sys.path
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))


def clear_overlays(driver: WebDriver) -> None:
    """Удаление баннеров через JS."""
    with allure.step("Очистка страницы"):
        try:
            script = """
            const sels = ['[class*="styles_container--"]',
                          '[class*="styles_overlay"]',
                          '.styles_rootInPortal__'];
            sels.forEach(s => document.querySelectorAll(s).forEach(e => {
                e.remove();
            }));
            document.body.style.overflow = 'auto';
            """
            driver.execute_script(script)
        except Exception:
            pass


@pytest.fixture
@allure.title("Настройка браузера")
def browser() -> WebDriver:
    """Инициализация Chrome."""
    opt = webdriver.ChromeOptions()
    opt.add_argument("--disable-blink-features=AutomationControlled")
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    opt.add_argument("--start-maximized")
    # Исправление E501: разбиваем длинную строку User-Agent
    ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0")
    opt.add_argument(f"user-agent={ua}")
    driver = webdriver.Chrome(options=opt)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', "
                  "{get: () => undefined})"
    })
    yield driver
    driver.quit()


@allure.feature("UI Тестирование Кинопоиска")
class TestKinopoiskUI:

    @pytest.mark.ui
    @allure.story("Поиск")
    @allure.title(f"1. Поиск фильма {MOVIE_TITLE}")
    def test_ui_search_gladiator_exact(self, browser: WebDriver) -> None:
        wait = WebDriverWait(browser, 30)
        with allure.step(f"Открытие {BASE_URL_UI}"):
            browser.get(BASE_URL_UI)
        with allure.step(f"Ввод {MOVIE_TITLE}"):
            sl = (By.CSS_SELECTOR, "input[name='kp_query']")
            search = wait.until(EC.presence_of_element_located(sl))
            clear_overlays(browser)
            search.send_keys(MOVIE_TITLE + Keys.ENTER)
        with allure.step("Проверка результатов"):
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "main")))
            assert SEARCH_QUERY.lower() in browser.page_source.lower()

    @pytest.mark.ui
    @allure.story("Usability")
    @allure.title("2. Проверка года в карточке")
    def test_ui_gladiator_card_year(self, browser: WebDriver) -> None:
        wait = WebDriverWait(browser, 30)
        browser.get(BASE_URL_UI)
        with allure.step(f"Поиск {SEARCH_QUERY}"):
            search = wait.until(EC.presence_of_element_located(
                (By.NAME, "kp_query")))
            search.send_keys(SEARCH_QUERY + Keys.ENTER)
        with allure.step(f"Проверка наличия '{MOVIE_STR_UI}'"):
            time.sleep(3)
            clear_overlays(browser)
            # Исправление E501: перенос элементов кортежа
            res_sel = (By.CSS_SELECTOR, "div.search_results, main")
            res = wait.until(EC.visibility_of_element_located(res_sel))
            assert MOVIE_STR_UI in res.text

    @pytest.mark.ui
    @allure.story("Совместимость")
    @allure.title("3. Адаптивность")
    def test_ui_mobile_search_adaptive(self, browser: WebDriver) -> None:
        browser.set_window_size(375, 812)
        browser.get(BASE_URL_UI)
        time.sleep(2)
        assert browser.find_element(By.TAG_NAME, "body").is_displayed()

    @pytest.mark.ui
    @allure.story("Контент")
    @allure.title("4. Наличие трейлера")
    def test_ui_gladiator_trailer_presence(self, browser: WebDriver) -> None:
        wait = WebDriverWait(browser, 30)
        browser.get(MOVIE_URL)
        time.sleep(3)
        clear_overlays(browser)
        # Исправление E501: разбиваем длинный XPath
        xp = ("//button[contains(., 'Трейлер')] | "
              "//a[contains(@href, 'video')]")
        btn = wait.until(EC.presence_of_element_located((By.XPATH, xp)))
        browser.execute_script("arguments[0].scrollIntoView();", btn)
        assert btn.is_displayed()

    @pytest.mark.ui
    @allure.story("Безопасность")
    @allure.title("5. Проверка HTTPS")
    def test_ui_security_https_gladiator(self, browser: WebDriver) -> None:
        browser.get(BASE_URL_UI)
        assert browser.current_url.startswith("https://")
