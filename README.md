# Selenium Pack

Удобный интерфейс для использования `Selenium`

## Вот как правильно подключать Selenium Pack

```python
from selenium_pack.lib import EBrowser, ViewSelenium


class ВашКласс(ViewSelenium):
    def run(self):
        """Действия после запуска браузера"""
        ...


if __name__ == '__main__':
    ВашКласс(
        # Путь к драйверу geckodriver
        executable_path=executable_path,
        # Путь к браузеру
        path_to_browser=EBrowser.Firefox.win_path_to_browser,
        # Какой браузер вы используете
        type_browser=EBrowser.Firefox,
    ).run()
```

## Возможности ViewSelenium

### Работа с Куки

- `set_cookies`
- `save_cookie`
- `read_cookie`

### Поиск HTML элементов

- `find_by_css_selector`
