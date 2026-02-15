from pages.login_page import LoginClass
from pages.book_details import BookDetails
from utils.excel_utils import read_data, write_data
from utils.logger_config import logger
import pytest
import time
import allure
import logging

@allure.title("Test valid book details")
@allure.testcase("TC-001")
@allure.description("Test valid book details")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Book Details Screen Test")
def test_valid_book_details(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    sheet_name = "Login"
    sheet_name2 = "Book Details"
    print("Excel Sheet Path", excel_sheet_path)
    
    with allure.step("Read login credentials from Excel"):
        email_cell = (2, 3) 
        password_cell = (2, 4)
        email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
        password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
        print("Email Read","=", email_read_from_excel)
        print("Password Read","=", password_read_from_excel)

    with allure.step("Read book details test data from Excel"):
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
    book_details_form = BookDetails(page)

    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    with allure.step("Enter book details and save"):
        response = book_details_form.validate_book_details_screen(
            book_title_read_from_excel,author_name_read_from_excel,
            publisher_name_read_from_excel,isbn_read_from_excel,
            total_copy_read_from_excel, available_copy_read_from_excel,member_expectedmsg_read_from_excel
            )
        allure.attach(
            body=str(response),
            name="Response Message",
            attachment_type=allure.attachment_type.TEXT
        )
    with allure.step("Validate expected message and update Excel result"):
        try:
            with allure.step("Validate Login and Book Details Save Messages"):
                assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
            write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=2, column=9, data=response)
        except AssertionError as e:
            write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=2, column=9, data=response)
            raise e