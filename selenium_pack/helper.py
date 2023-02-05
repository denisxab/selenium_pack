"""
Модуль с общим полезным функционалом
"""
from http.cookies import SimpleCookie


def parse_raw_cookies(text: str) -> list[dict[str, str]]:
    """
    Парсить формат из заголовка

    ```
    __ddg1_=Oqy7pqP1rJBKoVOTQBUs; redirect_host=spb.hh.ru; 
    ```

    """
    cookie = SimpleCookie()
    cookie.load(text)
    return [{"name": k, "value": v.value} for k, v in cookie.items()]


def parse_cookie_editor(obj: dict[str, str]) -> list[dict[str, str]]:
    """
    Парсить формат [Cookie-Editor](https://cookie-editor.cgagnier.ca/)

    ```
    [
        {
            "name": "_xsrf",
            "value": "9ba5bad4a91cf4c45ec01c5c1caa1faf",
            "domain": ".hh.ru",
            "hostOnly": false,
            "path": "/",
            "secure": true,
            "httpOnly": false,
            "sameSite": "no_restriction",
            "session": true,
            "firstPartyDomain": "",
            "partitionKey": null,
            "storeId": null
        }
    ]
    ```

    """
    return [{"name": i['name'], "value": i['value']} for i in obj]
