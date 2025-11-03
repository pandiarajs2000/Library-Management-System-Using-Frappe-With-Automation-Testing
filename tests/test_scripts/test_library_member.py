from pages.login_page import LoginClass
from tests.pages.library_member import LibraryMember
from utils.excel_utils import read_data, write_data
from utils.logger import logger
import pytest
import time
import allure

@allure.title("Test Valid Library Member")
@allure.testcase("TC-001")
@allure.description("Test Valid Library Member Details")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Library Member Screen Test")
def test_valid_login(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    # Login Datas Fetch from Excel.
    sheet_name = "Login"
    email_cell = (2, 3) 
    password_cell = (2, 4)
    expected_msg_cell = (2,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    # Library Member Form Data Fetch From Excel
    sheet_name2 = "Members"
    fullname_cell = (2,3)
    member_email_cell = (2,4)
    phone = (2,5)
    date_of_joining_cell = (2,6)
    status_cell = (2,7)
    member_expected_msg_cell = (2,8)

    member_fullname_read_from_excel = read_data(excel_sheet_path, sheet_name, *fullname_cell)
    member_email_read_from_excel = read_data(excel_sheet_path, sheet_name, *member_email_cell)
    member_phone_read_from_excel = read_data(excel_sheet_path, sheet_name, *phone)
    member_doj_read_from_excel = read_data(excel_sheet, sheet_name, *date_of_joining_cell)
    status_cell_read_from_excel = read_data(excel_sheet, sheet_name, *status_cell)
    member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *member_expected_msg_cell)


    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    
    library_member_form = LibraryMember(page)
    with allure.step("Open a Library Member Screen"):
        response = library_member_form.validate_library_member_screen(
            member_fullname_read_from_excel,member_email_read_from_excel,
            member_phone_read_from_excel,member_doj_read_from_excel,
            status_cell_read_from_excel,member_expectedmsg_read_from_excel
            )
    try:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        assert member_expectedmsg_read_from_excel in res, f"Expected message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=2, column=9, data=res)
    except Exception as e:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        assert member_expectedmsg_read_from_excel in res, f"Expected message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=2, column=9, data=res)