"""
Модуль с общим полезным функционалом
"""
from http.cookies import SimpleCookie
from email.parser import BytesParser


def parse_raw_cookies(text: str) -> list[dict[str, str]]:
    """
    Парсить формат из заголовка

    Вход:
    ```
    __ddg1_=Oqy7pqP1rJBKoVOTQBUs; redirect_host=spb.hh.ru; 
    ```

    Выход:
    ```
    [{"name": "Название","value": "Значение" }]
    ```
    """
    cookie = SimpleCookie()
    cookie.load(text)
    return [{"name": k, "value": v.value} for k, v in cookie.items()]


def parse_cookie_editor(obj: dict[str, str]) -> list[dict[str, str]]:
    """
    Парсить формат [Cookie-Editor](https://cookie-editor.cgagnier.ca/)

    Вход:
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

    Выход:
    ```
    [{"name": "Название","value": "Значение" }]
    ```
    """
    return [{"name": i['name'], "value": i['value']} for i in obj]


def parse_selenuim_to_request(cookies: list[dict[str, str]]) -> dict[str, str]:
    """
    Парсить формат selenuim в формат для request

    Вход:
    ```
    [{"name": "Название","value": "Значение" }]
    ```

    Вход:
    ```
    {"Название_1","Значение_1"}
    ```
    """

    return {i['name']: i['value'] for i in cookies}


def parse_raw_header(text: str) -> dict[str, str]:
    """
    Распарсить заголовки HTTP в словарь

    !! Убедитесь что text не имеет лишних отступов !!

    Вход:
    ```
    headers = parse_raw_header('''
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: ru,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://spb.hh.ru/search/vacancy?experience=between1And3&education=not_required_or_not_specified&schedule=remote&search_field=name&search_field=company_name&enable_snippets=true&salary=100000&text=Python&from=suggest_post&ored_clusters=true
DNT: 1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Connection: keep-alive
TE: trailers
''')
    ```

    Выход:
    ```
    {'User-Agent': 'Mozilla/5.0 (Windows...efox/109.0', ... }
    ```
    """
    _headers = BytesParser().parsebytes(
        b'\n'.join(x.encode('ascii') for x in text.split('\n') if x)
    )
    return dict(_headers)
