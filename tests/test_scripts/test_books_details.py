from pages.login_page import LoginClass
from pages.book_details import BookDetails
from utils.excel_utils import read_data, write_data
from utils.logger_config import logger
import pytest
import time
import allure
import logging

class TestBookDetails:
    @allure.title("Test valid book details")
    @allure.testcase("TC-001")
    @allure.description("Test valid book details")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Book Details Screen Test")
    def test_valid_book_details(self,page, excel_sheet,base_url):
        excel_sheet_path = excel_sheet
        print("Excel Sheet Path", excel_sheet_path)
        sheet_name = "Login"
        email_cell = (2, 3) 
        password_cell = (2, 4)
        email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
        password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
        print("Email Read","=", email_read_from_excel)
        print("Password Read","=", password_read_from_excel)
        sheet_name2 = "Book Details"
        book_title = (2,3)
        author_name = (2,4)
        publisher_name = (2,5)
        isbn = (2,6)
        total_copy = (2,7)
        available_copy = (2,8)
        member_expected_msg_cell = (2,9)

        book_title_read_from_excel = read_data(excel_sheet_path, sheet_name2, *book_title)
        author_name_read_from_excel = read_data(excel_sheet_path, sheet_name2, *author_name)
        publisher_name_read_from_excel = read_data(excel_sheet_path, sheet_name2, *publisher_name)
        isbn_read_from_excel = read_data(excel_sheet, sheet_name2, *isbn)
        total_copy_read_from_excel = read_data(excel_sheet, sheet_name2, *total_copy)
        available_copy_read_from_excel = read_data(excel_sheet, sheet_name2, *available_copy)
        member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name2, *member_expected_msg_cell)


        login_form = LoginClass(page)
        logger.info("Navigating to login page")
        with allure.step("Verify and Load the Site URL"):
            login_form.login_page_load(base_url)
        with allure.step("Enter credentials and submit login form"):
            res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
        book_details_form = BookDetails(page)
        with allure.step("Open a Book Details Screen"):
            response = book_details_form.validate_book_details_screen(
                book_title_read_from_excel,author_name_read_from_excel,
                publisher_name_read_from_excel,isbn_read_from_excel,
                total_copy_read_from_excel, available_copy_read_from_excel,member_expectedmsg_read_from_excel
                )
        try:
            with allure.step("Validate Login and Book Details Save Messages"):
                assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
            write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=2, column=9, data=response)
        except AssertionError as e:
            write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=2, column=9, data=response)
            raise e