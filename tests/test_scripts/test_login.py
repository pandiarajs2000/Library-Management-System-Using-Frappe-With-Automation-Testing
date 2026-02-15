from pages.login_page import LoginPage
from utils.excel_utils import read_data, write_data
from utils.logger_config import logger
import pytest
import allure

def test_valid_login(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (2, 3) 
    password_cell = (2, 4)
    expected_msg_cell = (2,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")
    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    page.wait_for_load_state("networkidle")
    logger.info(f"Actual result for valid login: {res}")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=2, column=6, data=res)

def test_invalid_login_with_email_password(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (3, 3) 
    password_cell = (3, 4)
    expected_msg_cell = (3,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")
    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    page.wait_for_load_state("networkidle")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=3, column=6, data=res)
    
def test_invalid_login_without_email(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (4, 3) 
    password_cell = (4, 4)
    expected_msg_cell = (4,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")
    
    email_empty_value = str(email_read_from_excel or "").strip()
    logger.info(f"Email Empty Value: {email_empty_value}")
    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_empty_value, password_read_from_excel)
    page.wait_for_load_state("networkidle")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=4, column=6, data=res)
    
def test_invalid_login_without_password(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (5, 3) 
    password_cell = (5, 4)
    expected_msg_cell = (5,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")
    password_empty_value = str(password_read_from_excel or "").strip()
    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_empty_value)
    page.wait_for_load_state("networkidle")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=5, column=6, data=res)
    
def test_invalid_login_with_useremail_as_number(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (6, 3) 
    password_cell = (6, 4)
    expected_msg_cell = (6,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")
    try:
        email_as_number = int(email_read_from_excel or 0)
    except ValueError:
        email_as_number = str(email_read_from_excel or "").strip()
    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_as_number, password_read_from_excel)
    page.wait_for_load_state("networkidle")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=6, column=6, data=res)
    
def test_invalid_login_without_useremail_password(page, excel_sheet,base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (7, 3) 
    password_cell = (7, 4)
    expected_msg_cell = (7,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")

    email_empty_value = str(email_read_from_excel or "").strip()
    password_empty_value = str(password_read_from_excel or "").strip()

    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_empty_value, password_empty_value)
    page.wait_for_load_state("networkidle")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=7, column=6, data=res)

@allure.title("Test Login Screen with Invalid Email Format")
@allure.testcase("TC-007")
@allure.description("Test Login Screen with Invalid Email Format")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login Form Test")
@allure.step("Verify and Load the Site URL")
def test_invalid_email_format(page, excel_sheet, base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (8, 3) 
    password_cell = (8, 4)
    expected_msg_cell = (8, 5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")
    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    page.wait_for_load_state("networkidle")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=8, column=6, data=res)

def test_password_with_special_characters(page, excel_sheet, base_url):
    excel_sheet_path = excel_sheet
    logger.info(f"Excel Sheet Path: {excel_sheet_path}")
    sheet_name = "Login"
    email_cell = (9, 3) 
    password_cell = (9, 4)
    expected_msg_cell = (9, 5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    logger.info(f"Email Read: {email_read_from_excel}")
    logger.info(f"Password Read: {password_read_from_excel}")
    login_form = LoginPage(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load(base_url)
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    page.wait_for_load_state("networkidle")
    if "Login Successful" not in res:
        allure.attach(page.screenshot(full_page=True), name="Login Failure Screenshot", attachment_type=allure.attachment_type.PNG)
    assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=9, column=6, data=res)