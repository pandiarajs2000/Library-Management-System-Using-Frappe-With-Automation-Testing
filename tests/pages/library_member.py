from playwright.sync_api import Page, expect
from utils.logger import logger
import traceback

class LibraryMember:
    def __init__(self, page: Page):
        self.page = page
        self.full_name_xpath = "//div[@data-fieldname='member_name']//input[@type='text']"
        self.email_xpath = "//div[@data-fieldname='email']//input[@type='text']"
        self.phone_xpath = "//div[@data-fieldname='phone']//input[@type='text']"
        self.date_of_join_xpath = "//input[@data-fieldtype='Date']"
        self.status_xpath = "//select[@type='text']"
        self.missing_fields_popup_xpath = "//div[@class='modal-body ui-front']/descendant::div[@class='msgprint']"
        self.save_btn_xpath = "//button[@data-label='Save']"
        self.search_box_xpath = "//input[@id='navbar-search']"
        self.add_library_member = "//button[@data-label='Add Library Member']"

    def validate_library_member_screen(self,fullname, email, phone, status, doj):
        try:
            logger.info("Attempting the Library Member Page")
            fullname = str(fullname or "").strip()
            email = str(email or "").strip()
            phone = int(phone or "")
            status = str(status or "").strip()
            doj = str(doj or "").strip()

            fullname_input = self.page.locator(self.full_name_xpath)
            fullname_input.clear()
            fullname_input.fill(fullname)

            email_input = self.page.locator(self.email_xpath)
            email_input.clear()
            email_input.fill(email)
            
            phone_input = self.page.locator(self.phone_xpath)
            phone_input.clear()
            phone_input.fill(email)

            status_input = self.page.locator(self.status_xpath)
            status_input.clear()
            status_input.select_option(status)

            doj_input = self.page.locator(self.date_of_join_xpath)
            doj_input.clear()
            doj_input.fill(doj)

            save_btn = self.page.locator(self.save_btn_xpath)
            save_btn.click()

        except Exception as e:
            traceback.print_exc()
            self.page.wait_for_timeout(3000)
            return f"Exception: {str(e)}"