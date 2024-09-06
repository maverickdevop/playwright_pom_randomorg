from playwright.sync_api import Page
from pages.base_methods import BaseMethods
import allure
import re


class GeneratorPage:

    MAIN_PAGE_URL = 'https://www.random.org/widgets/integers/iframe'
    TITLE = "RANDOM.ORG - Integer Widget"
    MIN_INPUT = "//input[contains(@id,'min')]"
    MAX_INPUT = "//input[contains(@id,'max')]"
    GENERATE_BUTTON = "//input[@value='Generate']"
    RESULT = "//span[contains(@id,'result')]"
    RESULT_NUM = "//span[contains(@id,'result')]//span"
    RESULT_RANGE = "//center[span[contains(text(), 'Min') and contains(text(), 'Max')]][normalize-space(.)]"

    def __init__(self, page: Page):
        self.method = BaseMethods(page)

    @allure.step("Переход на главную страницу Random.org")
    def get_randomorg_page(self):
        """ Переход на главную страницу Random.org """
        self.method.go_to_url(self.MAIN_PAGE_URL)

    @allure.step("Проверка заголовка страницы Random.org")
    def check_randomorg_page_title(self):
        """ Метод проверки title страницы Random.org """
        self.method.assert_title(self.TITLE)

    @allure.step("Ввод числовых значений в: {selector}, значения: {value}")
    def _set_input_values(self, selector, value):
        """ Внутренний метод для установки значений в input элементы """
        self.method.input_text(selector, str(value))

    @allure.step("Получение результата генерации")
    def _check_input_values(self):
        """ Внутренний метод проверки результата """
        try:
            result = self.method.get_element_number(self.RESULT_NUM)
            print("Результат сгенерированного значения:", result)
            yield result
        except Exception as e:
            raise AssertionError(f"Не удалось получить результат: {str(e)}")

    @allure.step("Установка значения 'От': {from_value}")
    def set_from_value(self, from_value):
        """ Установка значения 'От'
        :param from_value: Целочисленное значение От.
        """
        self._set_input_values(self.MIN_INPUT, from_value)

    @allure.step("Установка значения 'До': {to_value}")
    def set_to_value(self, to_value):
        """ Установка значения 'До'
        :param to_value: Целочисленное значение До.
        """
        self._set_input_values(self.MAX_INPUT, to_value)

    @allure.step("Заполнение диапазона данных: От={from_value}, До={to_value}")
    def fill_range_data(self, from_value, to_value):
        """ Метод ввода двух значений От и До """
        self.set_from_value(from_value)
        self.set_to_value(to_value)

    @allure.step("Клик на кнопку генерации значения")
    def click_generate_button(self):
        """ Клик на кнопку генерации рандомного значения """
        self.method.click_on_element(self.GENERATE_BUTTON)

    @allure.step("Ожидание появления результата")
    def wait_for_result(self):
        """ Проверка появления плашки с результатом (Сгенерированным значением) """
        self.method.wait_for_element(self.RESULT)

    @allure.step("Проверка ожидаемого результата: {expected_num}")
    def get_result_number_and_assert_with_expected_result(self, expected_num):
        """ Проверка полученного числа с ожидаемым
        :param expected_num: Ожидаемое целочисленное значение.
        """
        # Проверка на положительное число
        if not isinstance(expected_num, int) or expected_num <= 0:
            raise ValueError(f"Ожидаемое число {expected_num} должно быть положительным целым числом.")

        actual_num = next(self._check_input_values())

        assert expected_num == actual_num, \
            f"Полученное число {actual_num} не равно ожидаемому {expected_num}"

    @allure.step("Проверка результата в диапозоне списка значений: {expected_num}")
    def get_result_number_and_assert_with_expected_range(self, expected_num: list):
        """ Проверка полученного числа с диапазоном значений
        :param expected_num: Ожидаемый список целочисленных значений.
        """

        # Проверка на положительные числа в диапозоне
        if not all(isinstance(num, int) and num > 0 for num in expected_num):
            raise ValueError(f"В списке {expected_num} должны быть только положительные целые числа!")

        min_value, max_value = map(int, expected_num)
        actual_num = next(self._check_input_values())

        assert min_value <= actual_num <= max_value, \
            f"Полученное число {actual_num} не входит в диапазон от {min_value} до {max_value}"

    @allure.step("Проверка изменения числа 'До'")
    def check_input_number_changed(self):
        """ Проверка того, что введенное число 'До' изменилось."""

        # Получение текста блока результата
        result_text = self.method.get_element_text(self.RESULT_RANGE)

        patterns = {
           'min': r'Min:\s*(\d+)',
           'max': r'Max:\s*(\d+)'
        }

        matches = {}
        for name, pattern in patterns.items():
            match = re.search(pattern, result_text)
            if match:
                matches[name] = int(match.group(1))
            else:
                print(f"Не найдено значение {name} в тексте результата")

        if len(matches) == 2:
            extracted_min, extracted_max = matches['min'], matches['max']

            # Проверка изменения числа
            assert extracted_max == extracted_min + 1, \
                f"Измененное значение ({extracted_max}) не на 1 больше введенного {extracted_min}"

            actual_num = next(self._check_input_values())

            assert actual_num in [extracted_min, extracted_max], \
                f"Полученное рандомное значение ({actual_num}) не в диапозоне {[extracted_min, extracted_max]}"

        else:
            print("Не удалось найти оба значения (Min и Max) в блоке результата")
