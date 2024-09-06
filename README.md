# Playwright (Python) UI тесты сайта Random.org

Данные E2E UI написаны с использованием бибилиотеки Playwright
Для параметризации был использован подход Page Object Model (POM) для простоты распределения базовых методов и page для каждого типа тестов

Проект содержит набор UI тестов. Тесты разработаны для работы с различными моудлями и страницами проекта SEOWORK.
Используется паттерн `Page Object Model (POM)` - Каждый тест хранится в отдельном `page`, повторяющиеся методы стараемся выносить в отдельный метод с его тестовым классом.

Сами тесты лежат в `tests` в отдельной папке `generator`

## Системные требовнаия

Для корректной работы рекомендуется использовать OS: `MacOS Sonoma 14.5 и выше / Linux Ubuntu 20 и выше`
На остальных операционных системах запуски и корректность работы не тестировалась
Версия Python `Python 3.8 и выше` рекомендуется `Python 3.12` актуальноть можно проверить командой:

```bash
python -v
```

Установить актуальную версию можно тут: https://www.python.org/downloads/

Также все остальные пакеты, как `PyTest`, `Playwright` и т.д. можно из файла `requirements.txt`
Актуальная версия Playwright: https://playwright.dev/python/docs/intro

Для работы с кодом рекомендуется скачать IDE `PyCharm`
Бесплатная версия программы доступна на сайте JetBrains (Для примера ссылка на выгрузку CE версии MacOS ARM): https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=macM1&code=PCC

Дополнительно нужно установить Docker

1. Перейдите на официальный сайт Docker по этой ссылке: https://www.docker.com/products/docker-desktop/.
2. Нажмите кнопку Download for Mac. Docker Desktop доступен для macOS с чипами Intel и Apple Silicon (M1/M2) (Или другая ОС).
3. Проверьте установку Docker
```bash
docker --version
```
Если установка прошла успешно, вы увидите версию Docker, например:
```
Docker version 24.0.5, build 123abc
```


## Установка

Данная инструкция предназначена для локальной установки всех необходимых зависимостей
Для начала нужно склонировать репозиторий с тестами на свой ПК:

``` bash
git clone https://github.com/maverickdevop/playwright_pom_randomorg.git
```

Все актуальные изменения и версии кода на ветке `main`
Нужно своевременно подтягивать актуальный мастер на свой локальный ПК, дабы избежать конфликтов

Когда проект склонирован

Откройте в IDE PyCharm или любой другой IDE ваш проект
Обязательно создайте интерпритатор и виртуальное `venv` окружение Python, как указано ниже:

1. Создайте виртуальное окружение:

   - Для Mac OS/Win/Linux:
       ```bash
       python -m venv venv
       ```

2. Активируйте виртуальное окружение:

    - Для Windows:
        ```bash
        venv\Scripts\activate
        ```
    - Для Unix/MacOS:
        ```bash
        source venv/bin/activate
        ```

Или в правой нижней части IDE (По-умолчанию). Перейдите в Python Interpreter > Выберите версию Python > Нажмите OK (Виртульное окружение создастся по-умолчанию в корне проекта)
Затем установите все зависимости для работы с тестами, как ниже:

3. Установите зависимости из файла requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```

4. По сути все готово. Для запуска используем команду:
    ```bash
    pytest tests/
    ```
5. Дополнительно для генерации отчетов можно прописать:
    ```bash
    pytest tests/ --alluredir=allure-results
   allure serve allure-results
    ```

## Реализация тестирования

1. По сути в файле conftest.py в контексте браузера лежат cookie для обхода проверки на сайте Random.org
Файл с cookie есть в  `.env` в будущем обязательно его нужно добавть в `.gitignore` и прописать в Variabled GitHub


2. Для экономии времени проверки были только самого виджета, так как для переключения на iframe пришлось бы прописывать
дополнительные методы `frame_locator()`

## Дополнительно (Запуск тестов в Docker)

Тесты также были запакованы в Docker
Спуллить созданную версию можно с моего Docker Hub:
```bash
docker pull wenzelsmirnov95/randomorg:latest
```

Или по прямой ссылке: https://hub.docker.com/r/wenzelsmirnov95/randomorg

Также локально создать образ и запустить собранный образ в контейнере Docker
```bash
docker build -t randomorg .
docker run randomorg
```
