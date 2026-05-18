from pages.login_page import LoginPage
from pages.library_member import LibraryMember
from utils.excel_utils import get_library_member_data, get_login_data
import pytest
import allure


def login_to_application(page, base_url):
    login_data = get_login_data()
    user_email = login_data.get("email", "")
    password = login_data.get("password", "")

    login_page = LoginPage(page)
    login_page.login_page_load(base_url)
    login_page.login_screen_validate(user_email, password)


@allure.suite("Library Member Tests")
class TestLibraryMember:
    @pytest.mark.parametrize(
        "member_data",
        [data for data in get_library_member_data() if data.get("scenario") == "New" and data.get("expected") == "Saved"]
    )
    @allure.title("Validate successful library member creation")
    @allure.description("Verify that valid library member data is saved successfully.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_library_member_creation(self, page, base_url, member_data):
        with allure.step("Login to the application"):
            login_to_application(page, base_url)

        with allure.step("Submit valid library member data"):
            library_member_page = LibraryMember(page)
            result = library_member_page.validate_library_member_screen(
                member_data.get("member_name", ""),
                member_data.get("email", ""),
                member_data.get("phone", ""),
                member_data.get("date_of_joining", ""),
                member_data.get("status", ""),
                member_data.get("scenario", "New"),
                member_data.get("expected", "")
            )

        with allure.step("Verify success response"):
            assert result == member_data.get("expected"), f"Expected '{member_data.get('expected')}', got '{result}'"

    @pytest.mark.parametrize(
        "member_data",
        [data for data in get_library_member_data() if data.get("expected") != "Saved"]
    )
    @allure.title("Validate library member data and field-level failures")
    @allure.description("Verify that incomplete, invalid, or duplicate member inputs return the expected validation message.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_library_member_validations(self, page, base_url, member_data):
        with allure.step("Login to the application"):
            login_to_application(page, base_url)

        with allure.step("Submit invalid or duplicate library member data"):
            library_member_page = LibraryMember(page)
            result = library_member_page.validate_library_member_screen(
                member_data.get("member_name", ""),
                member_data.get("email", ""),
                member_data.get("phone", ""),
                member_data.get("date_of_joining", ""),
                member_data.get("status", ""),
                member_data.get("scenario", "New"),
                member_data.get("expected", "")
            )

        with allure.step("Verify expected validation message"):
            assert result == member_data.get("expected"), f"Expected '{member_data.get('expected')}', got '{result}'"
