import pytest
import os
import time
from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8001/#login"

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser


@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context()
    page = context.new_page()
    page.set_default_timeout(30000)
    yield page
    context.close()


@pytest.fixture
def excel_sheet():
    excel_path = "/home/pandiaraj/library_management/apps/library_management_system/tests/test_data_sheet.xlsx"
    return excel_path


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL