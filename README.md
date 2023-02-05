# Selenium Pack

Удобный интерфейс для использования `Selenium`

## Вот как правильно подключать Selenium Pack

```python
from selenium_pack.lib import EBrowser, ViewSelenium


class ВашКласс(ViewSelenium):
    def run_selenium(self):
        """Действия после запуска браузера"""
        ...


if __name__ == '__main__':
    executable_path = 'geckodriver.exe'

    ВашКласс(
        # Путь к драйверу geckodriver
        executable_path=executable_path,
        # Путь к браузеру
        path_to_browser=EBrowser.Firefox.win_path_to_browser,
        # Какой браузер вы используете
        type_browser=EBrowser.Firefox,
    ).run_selenium()
```

## Возможности ViewSelenium

### Работа с Куки

- `set_cookies`
- `save_cookie`
- `read_and_set_cookie`
- `read_cookie`

### Поиск HTML элементов

- `find_by_css_selector`

### Управление Драйвером через Tkinter

```python
from selenium_pack.lib import EBrowser, ViewSelenium, DriverBrowser
from selenium.webdriver.firefox.options import Options

class TkinterFromSelenium(ViewSelenium):

    def run_selenium(self):
        # Установить текст для поля информации
        self.TK_UpdateInfo('НовыйТекст')

    # Функция для обработки нажатия на пользовательскую кнопку
    def ФункцияОбработчикНажатия(): ...
    # Обработка нажатия на кнопку `Next`
    def TK_OnClickNext() : ...
    # Обработка нажатия на кнопку `Last`
    def TK_OnClickLast() : ...

if __name__ == '__main__':
    executable_path = 'geckodriver.exe'

    obj = TkinterFromSelenium(
        # Путь к драйверу geckodriver
        executable_path=executable_path,
        # Путь к браузеру
        path_to_browser=EBrowser.Firefox.win_path_to_browser,
        # Какой браузер вы используете
        type_browser=EBrowser.Firefox,
    )
    #
    obj.run_tkinter_and_selenium(
        # Список пользовательских кнопок
        tk_button={
            "Имя Для Кнопки": obj.ФункцияОбработчикНажатия
        }
    )
```
