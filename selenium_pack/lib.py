import pathlib
import pickle
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class EBrowser:
    """
    Настройки для разных браузеров
    """

    class Firefox:
        name = 'Firefox'
        # Путь к браузеру для Windows по умолчанию
        win_path_to_browser = r"C:\Program Files\Mozilla Firefox\firefox.exe"

    class Chrome:
        name = 'Chrome'
        """
        Установка Chrome драйвер на Linux
        
        1. sudo apt install chromium-chromedriver
        2. executable_path="/usr/lib/chromium-browser/chromedriver"
        """
        win_path_to_browser = "???"


class ViewSelenium:
    """

    - Перейти на указанную станицу = `self.browser.get('URL')`
    """
    # Путь для сохранения куки
    _PathSaveCookies = 'browser_cookies.pkl'

    def __init__(
        self,
        executable_path: str,
        path_to_browser: str,
        type_browser: EBrowser,
        options: Options = None,
        _PathSaveCookies: str | pathlib.Path = None
    ):
        """
        Инициализация браузера

        executable_path: Путь к драйверу geckodriver
        path_to_browser: Путь к браузеру
        options: Опции для браузера
        type_browser: Тип браузера

        ======================================================

        Скачать драйвер https://github.com/mozilla/geckodriver/releases/latest
        - linux:https://github.com/mozilla/geckodriver/releases/latest
        """
        # Путь для сохранения куки
        self._PathSaveCookies = _PathSaveCookies
        # Опции по умолчанию
        if not options:
            options = Options()
        # Путь к браузеру
        options.binary_location = path_to_browser
        self.browser: WebDriver
        # Создаем браузер
        match type_browser:
            case EBrowser.Firefox:
                self.browser = webdriver.Firefox(
                    executable_path=executable_path,
                    options=options
                )
            case EBrowser.Chrome:
                self.browser = webdriver.Chrome(
                    executable_path=executable_path,
                    options=options
                )
    ##
    # Работа с непосредственным браузером
    ##

    def close_browser(self):
        """
        Закрыть окно браузера
        """
        self.browser.close()
        self.browser.quit()
    ##
    # Куки
    ##

    def set_cookies(self, cookies: list[dict[str, str]]):
        """
        Вставить куки в страницу

        [{"name": "Название","value": "Значение" }]
        """
        for c in cookies:
            self.browser.add_cookie(c)
        self.browser.refresh()

    def save_cookie(self):
        """Сохраняем куки в файл `path_save_cookies` """
        pickle.dump(
            self.browser.get_cookies(),
            open(self._PathSaveCookies, 'wb')
        )

    def read_cookie(self):
        """Прочитать куки из файла `path_save_cookies`"""
        if pathlib.Path(self._PathSaveCookies).exists():
            self.set_cookies(pickle.load(open(self._PathSaveCookies, 'rb')))
        else:
            raise FileExistsError(
                f'Нет файла с куки: {pathlib.Path(self._PathSaveCookies).resolve()}, попробуйте сохранить кики в файл через метод `save_cookie`'
            )

    ##
    # Поиск HTML элементов
    ##

    def find_by_css_selector(
        self, css_selector: str, many: bool = False, elm: WebElement | WebDriver = None
    ) -> WebElement | list[WebElement]:
        """
        Получить элемент(Ы) по CSS селектору

        css_selector: CSS селектор
        elm: Элемент с которого начать поиск, по умолчанию с `document`
        many: Если True то вернет несколько записей, если False то вернет только одну
        """
        if not elm:
            elm = self.browser
        if many:
            return elm.find_elements(By.CSS_SELECTOR, css_selector)
        else:
            return elm.find_element(By.CSS_SELECTOR, css_selector)