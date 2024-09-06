from allure import step


class BaseMethods:
    def __init__(self, page):
        self.page = page

    @step("Переход на {url} веб-страницы")
    def go_to_url(self, url):
        """
        Метод для перехода на указанную URL.
        :param url: URL-параметр для перехода.
        """
        self.page.goto(url)
        return self

    @step("Получение title-заголовка текущей страницы и сравнение с {title}")
    def assert_title(self, title):
        """
        Метод для получения заголовка текущей страницы.
        :return: Заголовок страницы.
        :title: Проверяемый заголовок
        """
        page_title = self.page.title()
        assert title == page_title, f"Ожидаемый {title} не содержится в {page_title}"

    @step("Ожидание появления элемента с селектором {selector}")
    def wait_for_element(self, selector):
        """
        Метод для ожидания появления элемента на странице.
        :param selector: Селектор элемента для ожидания.
        """
        self.page.wait_for_selector(selector)
        return self

    @step("Клик по элементу с селектором {selector}")
    def click_on_element(self, selector):
        """
        Метод для клика по элементу по селектору.
        :param selector: Селектор элемента для клика.
        """
        self.page.click(selector)
        return self

    @step("Ввод текста {text} в инпут {selector}")
    def input_text(self, selector, text):
        """
        Метод для ввода текста в поле ввода по селектору.
        :param selector: Селектор поля ввода.
        :param text: Текст для ввода (может быть целым числом или строкой).
        """
        # Преобразуем text в строку, если это не уже
        self.page.fill(selector, str(text))
        return self

    @step("Ввод получения номера из элемента {selector}")
    def get_element_number(self, selector):
        """
        Метод получения числового значения из селектора.
        :param selector: Селектор поля со значением.
        :return: Текст из элемента или None, если элемент не найден.
        """
        result_element = self.page.wait_for_selector(selector)

        # Проверка наличия элемента
        if not result_element.is_visible():
            print(f"Элемент с селектором '{selector}' не найден.")
            return None

        # Извлечение текстового содержимого
        try:
            number_text = result_element.text_content()
        except Exception as e:
            print(f"Ошибка при извлечении текста: {str(e)}")
            return None

        # Обработка пустого текста
        if not number_text.strip():
            print("Текстовый контент элемента пуст.")
            return None

        # Разделение текста и извлечение числа
        lines = number_text.split('\n')
        if len(lines) < 1:
            print("Не удалось найти число в тексте.")
            return None
        try:
            number = int(lines[0].strip())
        except ValueError:
            print("Извлеченное значение не является целым числом.")
            return None
        return number

    @step("Ввод получения текста из элемента {selector}")
    def get_element_text(self, selector):
        """
        Метод получения текста из элемента по селектору.
        :param selector: Селектор элемента.
        :return: Текст из элемента или None, если элемент не найден.
        """
        result_element = self.page.wait_for_selector(selector)

        # Проверка наличия элемента
        if not result_element.is_visible():
            print(f"Элемент с селектором '{selector}' не найден.")
            return None

        # Извлечение текстового содержимого
        try:
            text = result_element.inner_text()
        except Exception as e:
            print(f"Ошибка при извлечении текста: {str(e)}")
            return None

        # Обработка пустого текста
        if not text.strip():
            print("Текстовое содержимое элемента пусто.")
            return None
        return text