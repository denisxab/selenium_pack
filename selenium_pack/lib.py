"""
Модуль для удобной работы с Selenium
"""
import pathlib
import pickle
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from typing import Callable
import threading
import tkinter as tk


class DriverBrowser:
    # Имя браузера
    name: str
    # Путь к браузеру для Windows по умолчанию
    win_path_to_browser: str

    def AntiBot(options: Options):
        """Метод для скрытия бота"""
        ...

    def new_options():
        """Создать новые опции для конкретного браузера"""
        ...


class EBrowser:
    """
    Настройки для разных браузеров
    """

    class Firefox(DriverBrowser):
        name = 'Firefox'
        win_path_to_browser = r"C:\Program Files\Mozilla Firefox\firefox.exe"

        def AntiBot(options: Options):
            options.add_argument(
                "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
            options.set_preference("dom.webdriver.enabled", False)
            return options

        def new_options() -> Options:
            return webdriver.FirefoxOptions()

    class Chrome(DriverBrowser):
        name = 'Chrome'
        """
        Установка Chrome драйвер на Linux
        
        1. sudo apt install chromium-chromedriver
        2. executable_path="/usr/lib/chromium-browser/chromedriver"
        """
        win_path_to_browser = "???"

        def AntiBot(options: Options):
            options.add_argument(
                "--disable-blink-features=AutomationControlled")
            return options

        def new_options() -> Options:
            return webdriver.ChromeOptions()


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
        type_browser: DriverBrowser,
        AntiBot=True,
        _options: Options = None,
        _PathSaveCookies: str | pathlib.Path = None,
    ):
        """
        Инициализация браузера

        executable_path: Путь к драйверу geckodriver
        path_to_browser: Путь к браузеру
        type_browser: Тип браузера
        AntiBot: Если True то будет применять настройки для скрытия бота
        _options: Опции для браузера
        _PathSaveCookies: Путь для сохранения куки

        ======================================================

        Скачать драйвер https://github.com/mozilla/geckodriver/releases/latest
        - linux:https://github.com/mozilla/geckodriver/releases/latest
        """
        # Путь для сохранения куки
        self._PathSaveCookies = _PathSaveCookies if _PathSaveCookies else self._PathSaveCookies
        # Опции по умолчанию для каждого браузера
        if not _options:
            _options = type_browser.new_options()
        # Если True то будет применять настройки для скрытия бота
        if AntiBot:
            type_browser.AntiBot(_options)
        # Путь к браузеру
        _options.binary_location = path_to_browser
        self.browser: WebDriver
        # Создаем браузер
        match type_browser:
            case EBrowser.Firefox:
                self.browser = webdriver.Firefox(
                    executable_path=executable_path,
                    options=_options
                )
            case EBrowser.Chrome:
                self.browser = webdriver.Chrome(
                    executable_path=executable_path,
                    options=_options
                )
        ##
        # Переменные который будут сохранять стояние браузера
        ##
        # Текущий URL. Он обновляется если открывать URL через метод `self.get(URL)`
        self.select_url: str = ''
        ##
        # Переменные для Tkinter
        ##
        # Хранения пользовательских кнопок для Tkinter
        self.user_buttons: dict[str, Callable] = {}
        # Поле для информации в Tkinter
        self.text_info: tk.Button | None = None

    def run_selenium(self):
        """
        Запуск логики для селениума
        """
        ...

    def run_tkinter_and_selenium(
        self,
        tk_button: dict[str, Callable] = None,
    ):
        """
        Запустить Tkinter

        tk_button: Кнопки взаимодействия  {"ИмяДляКнопки":ФункцияОбработчик}
        """
        def _wrap():
            """
            Логика для запуска Tkinter в отдельном потоке
            """
            tk_windows = tk.Tk()
            tk_windows.title("Tkinter From Selenium")
            #
            self.text_info = tk.Label(tk_windows, text="Поле для Информации")
            self.text_info.pack()
            # Кнопка назад
            button_last = tk.Button(tk_windows, text="Last",
                                command=self.TK_OnClickLast)
            button_last.pack()
            ##
            # Добавляем пользовательские кнопки в Tkinter. Добавленные кнопки сохраняться в переменную `user_buttons`
            ##
            if tk_button:
                for name_bt, func_bt in tk_button.items():
                    name_bt: str
                    func_bt: Callable
                    #
                    tmp_button1 = tk.Button(
                        tk_windows, text=name_bt, command=func_bt)
                    tmp_button1.pack()
                    #
                    self.user_buttons[name_bt] = func_bt
            # Кнопка вперед
            button_next = tk.Button(tk_windows, text="Next",
                                command=self.TK_OnClickNext)
            button_next.pack()
            #
            tk_windows.mainloop()

        # Запуск Tkinter в отдельном потоке
        tk_threading = threading.Thread(
            target=_wrap, args=(), name="Tk_Threading", daemon=True)
        tk_threading.start()
        # После запуска Tkinter в отдельном потоке, выполняем логику для Selenium
        self.run_selenium()
        # Не закрываем поток с Tkinter
        tk_threading.join()

    ##
    # Работа с непосредственным браузером
    ##

    def get(self, url: str):
        """Перейти на указанный Url в браузере"""
        # Переходим на указанный URL
        self.browser.get(url)
        # Обновляем текущий URL
        self.select_url = url

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
        self, css_selector: str, *, many: bool = False, is_wait: bool = True, _max_wait_time: float = 3.0, elm: WebElement | WebDriver = None
    ) -> WebElement | list[WebElement]:
        """
        Получить элемент(Ы) по CSS селектору

        css_selector: CSS селектор
        elm: Элемент с которого начать поиск, по умолчанию с `document`
        many: Если True то вернет несколько записей, если False то вернет только одну
        is_wait: Если True то будет ждать появления элемента в DOM дереве
        _max_wait_time: Сколько(секунд) максимум ожидать
        """
        if not elm:
            elm = self.browser

        if many:
            if is_wait:
                # Сколько максимум ждать
                wait = WebDriverWait(elm, _max_wait_time)
                # Ожидать пока элемент загрузиться (Ожидание проверки того, что элемент присутствует в DOM страницы и виден. )
                # https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
                # visibility_of_all_elements_located - Все видны
                # visibility_of_any_elements_located - Виден хотя бы один
                return wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
            else:
                return elm.find_elements(By.CSS_SELECTOR, css_selector)
        else:
            if is_wait:
                # Сколько максимум ждать
                wait = WebDriverWait(elm, _max_wait_time)
                # Ожидать пока элемент загрузиться (Ожидание проверки того, что элемент присутствует в DOM страницы и виден. )
                # https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
                return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            else:
                return elm.find_element(By.CSS_SELECTOR, css_selector)

    ##
    # Для Tkinter
    ##

    def TK_OnClickNext(self):
        """Обработчик события нажатия кнопки вперед(вправо)"""
        ...

    def TK_OnClickLast(self):
        """Обработчик события нажатия кнопки назад(влево)"""
        ...

    def TK_UpdateInfo(self, text: str):
        """Вставить указанный текст в поле для информации"""
        print('TK_UpdateInfo:\t', text)
        self.text_info.config(text=text)
