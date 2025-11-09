from pages.login_page import LoginClass
from pages.library_member import LibraryMember
from utils.excel_utils import read_data, write_data
from utils.logger_config import logger
import pytest
import time
import allure
import logging


@allure.title("Test Valid Library Member")
@allure.testcase("TC-001")
@allure.description("Test Valid Library Member Details")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Library Member Screen Test")
def test_valid_member_data(page, excel_sheet,base_url):
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

    member_fullname_read_from_excel = read_data(excel_sheet_path, sheet_name2, *fullname_cell)
    member_email_read_from_excel = read_data(excel_sheet_path, sheet_name2, *member_email_cell)
    member_phone_read_from_excel = read_data(excel_sheet_path, sheet_name2, *phone)
    member_doj_read_from_excel = read_data(excel_sheet, sheet_name2, *date_of_joining_cell)
    status_cell_read_from_excel = read_data(excel_sheet, sheet_name2, *status_cell)
    print("Status:", status_cell_read_from_excel)
    member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name2, *member_expected_msg_cell)


    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    scenario = "New"
    library_member_form = LibraryMember(page)
    with allure.step("Open a Library Member Screen"):
        response = library_member_form.validate_library_member_screen(
            member_fullname_read_from_excel,member_email_read_from_excel,
            member_phone_read_from_excel,member_doj_read_from_excel,
            status_cell_read_from_excel, scenario
            )
    try:
        with allure.step("Validate Login and Member Save Messages"):
            assert expectedmsg_read_from_excel in res, f"Expected Login message: '{expectedmsg_read_from_excel}', but got: '{res}'"
            assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=2, column=9, data=response)
    except AssertionError as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=2, column=9, data=response)
        raise e
    
@allure.title("Test the Existing Member Email ID Should not be Allowed.")
@allure.testcase("TC-002")
@allure.description("Test the Existing Member Email ID Should not be Allowed.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Test the Negative scenario for the existing member email id should not allowed.")
def test_duplicate_validation_for_email(page, excel_sheet,base_url):
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
    fullname_cell = (3,3)
    member_email_cell = (3,4)
    phone = (3,5)
    date_of_joining_cell = (3,6)
    status_cell = (3,7)
    member_expected_msg_cell = (3,8)

    member_fullname_read_from_excel = read_data(excel_sheet_path, sheet_name2, *fullname_cell)
    member_email_read_from_excel = read_data(excel_sheet_path, sheet_name2, *member_email_cell)
    member_phone_read_from_excel = read_data(excel_sheet_path, sheet_name2, *phone)
    member_doj_read_from_excel = read_data(excel_sheet, sheet_name2, *date_of_joining_cell)
    status_cell_read_from_excel = read_data(excel_sheet, sheet_name2, *status_cell)
    print("Status:", status_cell_read_from_excel)
    member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name2, *member_expected_msg_cell)
    scenario = "Duplicate"
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
            status_cell_read_from_excel, scenario
            )
    try:
        with allure.step("Validate Login and Existing Member Should not be allowed."):
            assert expectedmsg_read_from_excel in res, f"Expected Login message: '{expectedmsg_read_from_excel}', but got: '{res}'"
            assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=3, column=9, data=response)
    except AssertionError as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=3, column=9, data=response)

@allure.title("Test the Existing Member phone number Should not be Allowed.")
@allure.testcase("TC-003")
@allure.description("Test the Existing Member phone number Should not be Allowed.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Test the Negative scenario for the existing member phone number should not allowed.")
def test_duplicate_validation_for_phone_no(page, excel_sheet,base_url):
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
    fullname_cell = (4,3)
    member_email_cell = (4,4)
    phone = (4,5)
    date_of_joining_cell = (4,6)
    status_cell = (4,7)
    member_expected_msg_cell = (4,8)

    member_fullname_read_from_excel = read_data(excel_sheet_path, sheet_name2, *fullname_cell)
    member_email_read_from_excel = read_data(excel_sheet_path, sheet_name2, *member_email_cell)
    member_phone_read_from_excel = read_data(excel_sheet_path, sheet_name2, *phone)
    member_doj_read_from_excel = read_data(excel_sheet, sheet_name2, *date_of_joining_cell)
    status_cell_read_from_excel = read_data(excel_sheet, sheet_name2, *status_cell)
    print("Status:", status_cell_read_from_excel)
    member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name2, *member_expected_msg_cell)
    scenario = "Duplicate"
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
            status_cell_read_from_excel, scenario
            )
    try:
        with allure.step("Validate Login and Existing Member Should not be allowed."):
            assert expectedmsg_read_from_excel in res, f"Expected Login message: '{expectedmsg_read_from_excel}', but got: '{res}'"
            assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=4, column=9, data=response)
    except AssertionError as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=4, column=9, data=response)


@allure.title("Test without fullname field while save it should be throwing an error.")
@allure.testcase("TC-004")
@allure.description("Test without fullname field while save it should be throwing an error.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Test without fullname field while save it should be throwing an error.")
def test_without_fullname_validation(page, excel_sheet,base_url):
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
    fullname_cell = (5,3)
    member_email_cell = (5,4)
    phone = (5,5)
    date_of_joining_cell = (5,6)
    status_cell = (5,7)
    member_expected_msg_cell = (5,8)

    member_fullname_read_from_excel = read_data(excel_sheet_path, sheet_name2, *fullname_cell)
    member_email_read_from_excel = read_data(excel_sheet_path, sheet_name2, *member_email_cell)
    member_phone_read_from_excel = read_data(excel_sheet_path, sheet_name2, *phone)
    member_doj_read_from_excel = read_data(excel_sheet, sheet_name2, *date_of_joining_cell)
    status_cell_read_from_excel = read_data(excel_sheet, sheet_name2, *status_cell)
    print("Status:", status_cell_read_from_excel)

    empty_value_for_fullname = str(member_fullname_read_from_excel or "").strip()

    member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name2, *member_expected_msg_cell)
    scenario = "New"
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    
    library_member_form = LibraryMember(page)
    with allure.step("Open a Library Member Screen"):
        response = library_member_form.validate_library_member_screen(
            empty_value_for_fullname,member_email_read_from_excel,
            member_phone_read_from_excel,member_doj_read_from_excel,
            status_cell_read_from_excel, scenario
            )
    try:
        with allure.step("Validate Login and Existing Member Should not be allowed."):
            assert expectedmsg_read_from_excel in res, f"Expected Login message: '{expectedmsg_read_from_excel}', but got: '{res}'"
            assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=5, column=9, data=response)
    except AssertionError as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=5, column=9, data=response)

@allure.title("Test without emailid field while save it should be throwing an error.")
@allure.testcase("TC-005")
@allure.description("Test without emailid field while save it should be throwing an error.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Test without emailid field while save it should be throwing an error.")
def test_without_emailid_validation(page, excel_sheet,base_url):
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
    fullname_cell = (6,3)
    member_email_cell = (6,4)
    phone = (6,5)
    date_of_joining_cell = (6,6)
    status_cell = (6,7)
    member_expected_msg_cell = (6,8)

    member_fullname_read_from_excel = read_data(excel_sheet_path, sheet_name2, *fullname_cell)
    member_email_read_from_excel = read_data(excel_sheet_path, sheet_name2, *member_email_cell)
    member_phone_read_from_excel = read_data(excel_sheet_path, sheet_name2, *phone)
    member_doj_read_from_excel = read_data(excel_sheet, sheet_name2, *date_of_joining_cell)
    status_cell_read_from_excel = read_data(excel_sheet, sheet_name2, *status_cell)
    print("Status:", status_cell_read_from_excel)

    empty_value_for_email = str(member_email_read_from_excel or "").strip()

    member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name2, *member_expected_msg_cell)
    scenario = "New"
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    
    library_member_form = LibraryMember(page)
    with allure.step("Open a Library Member Screen"):
        response = library_member_form.validate_library_member_screen(
            member_fullname_read_from_excel,empty_value_for_email,
            member_phone_read_from_excel,member_doj_read_from_excel,
            status_cell_read_from_excel, scenario
            )
    try:
        with allure.step("Validate Login and Existing Member Should not be allowed."):
            assert expectedmsg_read_from_excel in res, f"Expected Login message: '{expectedmsg_read_from_excel}', but got: '{res}'"
            assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=6, column=9, data=response)
    except AssertionError as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=6, column=9, data=response)

@allure.title("To verify the existing member mobile number should not be allowed.")
@allure.testcase("TC-006")
@allure.description("To verify the existing member mobile number should not be allowed.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("To verify the existing member mobile number should not be allowed.")
def test_without_emailid_and_fullname_validation(page, excel_sheet,base_url):
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
    fullname_cell = (7,3)
    member_email_cell = (7,4)
    phone = (7,5)
    date_of_joining_cell = (7,6)
    status_cell = (7,7)
    member_expected_msg_cell = (7,8)

    member_fullname_read_from_excel = read_data(excel_sheet_path, sheet_name2, *fullname_cell)
    member_email_read_from_excel = read_data(excel_sheet_path, sheet_name2, *member_email_cell)
    member_phone_read_from_excel = read_data(excel_sheet_path, sheet_name2, *phone)
    member_doj_read_from_excel = read_data(excel_sheet, sheet_name2, *date_of_joining_cell)
    status_cell_read_from_excel = read_data(excel_sheet, sheet_name2, *status_cell)
    print("Status:", status_cell_read_from_excel)

    empty_value_for_fullname = str(member_fullname_read_from_excel or "").strip()

    member_expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name2, *member_expected_msg_cell)
    scenario = "New"
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    
    library_member_form = LibraryMember(page)
    with allure.step("Open a Library Member Screen"):
        response = library_member_form.validate_library_member_screen(
            empty_value_for_fullname,member_email_read_from_excel,
            member_phone_read_from_excel,member_doj_read_from_excel,
            status_cell_read_from_excel, scenario
            )
    try:
        with allure.step("Validate Login and Existing Member Should not be allowed."):
            assert expectedmsg_read_from_excel in res, f"Expected Login message: '{expectedmsg_read_from_excel}', but got: '{res}'"
            assert member_expectedmsg_read_from_excel in response, f"Expected Member message: '{member_expectedmsg_read_from_excel}', but got: '{response}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=7, column=9, data=response)
    except AssertionError as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name2, row=7, column=9, data=response)