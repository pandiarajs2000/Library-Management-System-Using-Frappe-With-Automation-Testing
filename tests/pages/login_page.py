from utils.logger_config import logger
from playwright.sync_api import Page, expect
import time
import traceback
import os

class LoginPage:
    """Page object for handling login functionality in the application."""

    def __init__(self, page: Page):
        self.page = page
        self.email_field_xpath = "//form/descendant::input[@id='login_email']"
        self.password_field_xpath = "//form/descendant::input[@id='login_password']"
        self.password_show_xpath = "//form[contains(@class, 'form-signin') and contains(@class, 'form-login')]/descendant::div[@class='password-field']//span"
        self.login_btn_xpath = "//button[normalize-space()='Login']"
        self.popup_input = "//div[@class='form-group']/descendant::input[contains(@data-fieldname, 'password')]"
        self.popup_password_show = "//div[@class='form-group']/descendant::div[@class='toggle-password']"
        self.popup_submit_btn = "//div[@class='form-group']/descendant::button[contains(@data-fieldname, 'submit')]"
        self.popup_label = "//div[@class='form-group']/child::div[@class='clearfix']//label[@class='control-label reqd']"
        self.login_fail_text = "//button[normalize-space()='Invalid Login. Try again.']"
        self.apps_popup_xpath = "//a[@href='/app/home']"

    # login function
    def login_page_load(self, base_url):
        """Navigate to the login page and return the current URL.

        Args:
            base_url (str): The base URL to navigate to.

        Returns:
            str: The current page URL or an exception message.
        """
        try:
            url = base_url
            logger.info(f"Navigating to login page: {url}")
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle")
            site_url = self.page.url
            return site_url
        except Exception as e:
            logger.error(f"Error while loading login page: {str(e)}")
            traceback.print_exc()
            return f"Exception: {str(e)}"
    
    # login form field access
    def login_screen_validate(self, user_email, password):
        """Fill login credentials, submit, and validate the result.

        Args:
            user_email (str): The user's email.
            password (str): The user's password.
            expected_result (str): Expected outcome (currently unused).

        Returns:
            str: Validation message, error text, or "Login Successful".
        """
        try:
            logger.info(f"Attempting login with Email: {user_email}")
            user_email = str(user_email or "").strip()
            password = str(password or "").strip()
            # Fill credentials
            email_field = self.page.locator(self.email_field_xpath)
            password_field = self.page.locator(self.password_field_xpath)

            email_field.clear()
            password_field.clear()

            email_field.fill(user_email)
            password_field.fill(password)

            expect(self.page).to_have_url(self.page.url)  # Wait for page stability

            email_valid = email_field.evaluate("el => el.validity.valid")
            logger.info(f"Email validity check: {email_valid}")
            password_valid = password_field.evaluate("el => el.validity.valid")
            logger.info(f"Password validity check: {password_valid}")

            # email field validation
            if not email_valid:
                validation_msg = email_field.evaluate("el => el.validationMessage")
                logger.info(f"Email validation message: {validation_msg}")
                return validation_msg
            
            # password field validation 
            if not password_valid:
                validation_msg = password_field.evaluate("el => el.validationMessage")
                logger.info(f"Password validation message: {validation_msg}")
                return validation_msg
            
            login_btn = self.page.locator(self.login_btn_xpath)
            login_btn.click()
            logger.info("Clicked login button.")

            error_button_check = self.page.locator(self.login_fail_text)
            apps_popup = self.page.locator(self.apps_popup_xpath)

            expect(self.page).to_have_url(self.page.url)  # Wait for potential redirect

            if error_button_check.is_visible(timeout=5000):
                actual_text = error_button_check.text_content().strip()
                logger.info(f"Login failed: {actual_text}")
                return actual_text
            
            if apps_popup.is_visible():
                apps_popup.click()
            expect(self.page).to_have_title("Users")
            return "Users"
        except Exception as e:
            traceback.print_exc()
            expect(self.page).to_have_url(self.page.url)  # Fallback wait
            return f"Exception: {str(e)}"