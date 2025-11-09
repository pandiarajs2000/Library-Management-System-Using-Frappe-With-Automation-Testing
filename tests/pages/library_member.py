from playwright.sync_api import Page, expect
from utils.logger_config import logger
from datetime import datetime, timedelta
import traceback
import time

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
        self.member_id_xpath = "//li[@class='disabled']//a[starts-with(text(), 'MEMBER-')]"
        self.error_popup_xpath = "//div[@class='msgprint']"

    def validate_library_member_screen(self,fullname, email, phone, doj,status, scenario):
        
        try:
            logger.info("Search the Library Member List")
            search_input = self.page.locator(self.search_box_xpath)
            search_input.fill("Library Member")
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

            print("Date Value", type(doj))
            
            fullname_input = self.page.locator(self.full_name_xpath)
            fullname_input.clear()
            fullname_input.fill(fullname)

            email_input = self.page.locator(self.email_xpath)
            email_input.clear()
            email_input.fill(email)
            
            phone_input = self.page.locator(self.phone_xpath)
            phone_input.clear()
            phone_input.fill(phone)

            print("Date Value", doj, type(doj))

            if isinstance(doj, datetime):
                date_str = doj.strftime("%d-%m-%Y")
            else:
                date_str = str(doj).split(" ")[0].strip()

            print("Final Date Value to fill:", date_str)

            doj_input = self.page.locator(self.date_of_join_xpath)
            doj_input.click()
            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Backspace")
            self.page.keyboard.type(date_str)
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
                member_id = self.page.locator(self.member_id_xpath)
                popup_message = member_id.inner_text()
                logger.info(f"member id text {popup_message}")
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"//home//pandiaraj//library_management//apps//library_management_system//tests//screenshots//member_data_save_{timestamp}.png"
                self.page.screenshot(path=screenshot_path)
                logger.info(f"Document saved successfully via page indicator.{popup_message}")

            except:
                error_popup = self.page.locator(self.error_popup_xpath)
                try:
                    popup_message = error_popup.inner_text().strip()
                    self.page.wait_for_timeout(state="visible", timeout=5000)
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"//home//pandiaraj//library_management//apps//library_management_system//tests//screenshots//failed_one_{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)
                    logger.info(f"Error Message : {popup_message}")
                    logger.error("This member is already exists in the library members list.")
                except Exception as e:
                    popup_message = error_popup.inner_text().strip()
                    logger.warning(f"{popup_message}")
            
            if scenario == "New":
                if "MEMBER-" in popup_message:
                    print("Scenario", scenario)
                    return "Saved"
                else:
                    logger.error(f"While saving the new member = {popup_message}")
                    assert False, f"expected 'Saved' but got '{popup_message}' "
            elif scenario == "Duplicate":
                if "MEMBER-" in popup_message:
                    print("Scenario", scenario)
                    print("DEFECT: Duplicate member was saved successfullt - Validation is message is not shown.")
                    logger.error("DEFECT: Duplicate member was saved successfullt - Validation is message is not shown.")
                    assert False, f"DEFECT: Duplicate member was saved successfullt - Validation is message is not shown."
                elif "exists" in popup_message.lower() or "duplicate" in popup_message.lower():
                    logger.info("Validation worked correctly — duplicate member not allowed.")
                    return "This member already exists"
                else:
                    logger.warning(f"Unexpected message for duplicate scenario: {popup_message}")
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"//home//pandiaraj//library_management//apps//library_management_system//tests//screenshots//failed_two_{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)
                    return "Mandatory for Some Fields."
            else:
                logger.warning(f"Invalid scenario: {scenario}")
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"//home//pandiaraj//library_management//apps//library_management_system//tests//screenshots//failed_three_{timestamp}.png"
                self.page.screenshot(path=screenshot_path)
                return "Invalid Scenario"

        except Exception as e:
            traceback.print_exc()
            self.page.wait_for_timeout(3000)
            return f"Exception: {str(e)}"