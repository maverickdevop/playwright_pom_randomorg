from pages.generator_page import GeneratorPage
import pytest
import os


class TestGenerateValues:

    @pytest.fixture(autouse=True)
    def setup_class(self, page):
        self.generator = GeneratorPage(page)
        self.generator.get_randomorg_page()
        self.generator.check_randomorg_page_title()

    def test_input_range_numbers(self):
        self.generator.fill_range_data(10, 100)
        self.generator.click_generate_button()
        self.generator.wait_for_result()
        self.generator.get_result_number_and_assert_with_expected_range([1, 100])

    def test_input_close_range_numbers(self):
        self.generator.fill_range_data(1, 1)
        self.generator.click_generate_button()
        self.generator.wait_for_result()
        self.generator.get_result_number_and_assert_with_expected_result(1)

    def test_input_close_range_numbers_and_check_changed_result(self):
        self.generator.fill_range_data(23, 13)
        self.generator.click_generate_button()
        self.generator.wait_for_result()
        self.generator.check_input_number_changed()