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
        self.status_xpath = "//select[@data-fieldname='status']"
        self.missing_fields_popup_xpath = "//div[@class='modal-body ui-front']/descendant::div[@class='msgprint']"
        self.save_btn_xpath = "//button[@data-label='Save']"
        self.search_box_xpath = "//input[@id='navbar-search']"
        self.add_library_member = "//button[@data-label='Add Library Member']"
        self.save_doc_id = "//li[@class='disabled']//a"

    def validate_library_member_screen(self,fullname, email, phone, doj,status):
        try:
            logger.info("Search the Library Member List")
            search_input = self.page.locator(self.search_box_xpath)
            search_input.fill("Library Member List")
            search_input.press("ArrowDown")
            self.page.wait_for_timeout(500)
            search_input.press("Enter")

            logger.info("Click the Add New Libary Member Button")
            add_new_btn = self.page.locator(self.add_library_member)
            add_new_btn.click()

            logger.info("Attempting the Library Member Page")
            fullname = str(fullname or "").strip()
            email = str(email or "").strip()
            phone = str(phone or "")
            status = str(status or "").strip()
            doj = str(doj or "").strip()

            print("Status Value",status)

            fullname_input = self.page.locator(self.full_name_xpath)
            fullname_input.clear()
            fullname_input.fill(fullname)

            email_input = self.page.locator(self.email_xpath)
            email_input.clear()
            email_input.fill(email)
            
            phone_input = self.page.locator(self.phone_xpath)
            phone_input.clear()
            phone_input.fill(phone)

            doj_input = self.page.locator(self.date_of_join_xpath)
            doj_input.click()
            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Backspace")
            self.page.keyboard.type(doj)
            self.page.keyboard.press("Tab") 

            status_select = self.page.locator(self.status_xpath)
            status_select.wait_for(state="visible", timeout=5000)
            status_select.select_option(label=status)
            expect(status_select).to_have_value(status)


            save_btn = self.page.locator(self.save_btn_xpath)
            save_btn.click()
            self.page.wait_for_timeout(500)

            popup_message=""
            try:
                saved_label = self.page.locator(self.save_doc_id)
                saved_label.wait_for(state="visible", timeout=5000)
                popup_message = "Saved"
                logger.info("Document saved successfully via page indicator.")
            except:
                logger.warning("Document was not saved.")
            
            if "Saved" in popup_message:
                return "Saved"
            else:
                return "Mandatory for Some Fields."

        except Exception as e:
            traceback.print_exc()
            self.page.wait_for_timeout(3000)
            return f"Exception: {str(e)}"