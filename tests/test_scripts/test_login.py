from pages.login_page import LoginPage
from utils.excel_utils import get_login_data
from utils.logger_config import logger
from playwright.sync_api import expect
import pytest
import allure


@allure.suite("Login Tests")
class TestLogin:
    @allure.title("Validate Login Functionality")
    def test_login(self, page, base_url):
        login_data = get_login_data()
        user_email = login_data.get("email", "")
        password = login_data.get("password", "")
        expected_page_title = login_data.get("expected_page_title", "")
        login_page = LoginPage(page)
        login_page.login_page_load(base_url)
        login_page.login_screen_validate(user_email, password)
        title = page.title()
        logger.info(f"Page title after login attempt: {title}")
        expect(page).to_have_title(expected_page_title)