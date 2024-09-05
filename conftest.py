import argparse
import os
import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from datetime import datetime, timedelta

default_browser = "chromium"


@pytest.fixture(scope="session")
def browser_type(request):
    """Фикстура для выбора типа браузера. По умолчанию: Chromium"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser')
    args = parser.parse_known_args()[0]
    browser_option = args.browser
    return browser_option if browser_option else default_browser


@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    """Фикстура для настройки параметров запуска браузера."""
    launch_args = {
        "headless": False,
    }
    return launch_args


@pytest.fixture(scope="session")
def browser(browser_type, browser_type_launch_args):
    """Фикстура для запуска браузера."""
    with sync_playwright() as p:
        load_dotenv()
        if browser_type == "chromium":
            browser = p.chromium.launch(**browser_type_launch_args)
        elif browser_type == "firefox":
            browser = p.firefox.launch(**browser_type_launch_args)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def context(browser):
    """Фикстура для создания нового контекста браузера с куками."""
    context = browser.new_context(
        java_script_enabled=True,
        # Чтобы запруфать, что куки работают поменять URL, раскомментить запись видео
        # record_video_dir="tests/videos",
        # record_video_size={"width": 1200, "height": 700}
    )
    cookies = [
        {
            'name': 'RDOSESSION',
            'value': os.getenv('COOKIE'),
            'domain': '.random.org',
            'path': '/',
            'expires': int(datetime.now().timestamp()) + timedelta(days=365).total_seconds(),
            'httpOnly': False,
            'secure': True,
            'sameSite': "Lax"
        },
        {
            'name': 'RDOPRIVACY',
            'value': '%5Btrue%2Ctrue%2Ctrue%5D',
            'domain': '.random.org',
            'path': '/',
            'expires': int(datetime.now().timestamp()) + timedelta(days=365).total_seconds(),
            'httpOnly': False,
            'secure': False,
            'sameSite': "Lax"
        }
    ]
    context.add_cookies(cookies)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Фикстура для создания новой страницы."""
    page = context.new_page()
    yield page
    page.close()
