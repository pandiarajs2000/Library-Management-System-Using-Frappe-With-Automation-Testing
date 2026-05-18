from playwright.sync_api import Page, expect
from utils.logger_config import logger
from datetime import datetime
import traceback
import time
import os


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

    def _read_popup_message(self):
        error_popup = self.page.locator(self.error_popup_xpath)
        if error_popup.is_visible(timeout=3000):
            return error_popup.inner_text().strip()
        return ''

    def validate_library_member_screen(self, fullname, email, phone, doj, status, scenario, member_expectedmsg_read_from_excel):
        try:
            logger.info('Search the Library Member List')
            search_input = self.page.locator(self.search_box_xpath)
            search_input.fill('Library Member')
            search_input.press('ArrowDown')
            self.page.wait_for_timeout(500)
            search_input.press('Enter')

            logger.info('Click the Add New Library Member Button')
            self.page.locator(self.add_library_member).click()

            fullname = str(fullname or '').strip()
            email = str(email or '').strip()
            phone = str(phone or '').strip()
            status = str(status or '').strip()

            fullname_input = self.page.locator(self.full_name_xpath)
            fullname_input.fill('')
            fullname_input.fill(fullname)

            email_input = self.page.locator(self.email_xpath)
            email_input.fill('')
            email_input.fill(email)

            phone_input = self.page.locator(self.phone_xpath)
            phone_input.fill('')
            phone_input.fill(phone)

            if isinstance(doj, datetime):
                date_str = doj.strftime('%Y-%m-%d')
            else:
                date_str = str(doj or '').split(' ')[0].strip()

            doj_input = self.page.locator(self.date_of_join_xpath)
            doj_input.click()
            doj_input.fill('')
            if date_str:
                doj_input.fill(date_str)
                self.page.keyboard.press('Tab')

            if status:
                status_select = self.page.locator(self.status_xpath)
                status_select.wait_for(state='visible', timeout=5000)
                status_select.select_option(label=status)
                expect(status_select).to_have_value(status)

            self.page.locator(self.save_btn_xpath).click()
            self.page.wait_for_timeout(1000)

            member_id = ''
            popup_message = ''

            # Prefer success path first
            try:
                self.page.locator(self.save_doc_id).wait_for(state='visible', timeout=5000)
                member_id = self.page.locator(self.member_id_xpath).inner_text().strip()
                popup_message = member_id
                logger.info(f'member id text {popup_message}')
                screenshot_path = os.path.join('tests', 'screenshots', f"member_data_save_{time.strftime('%Y%m%d_%H%M%S')}.png")
                self.page.screenshot(path=screenshot_path)
                logger.info('Document saved successfully via page indicator.')
            except Exception:
                popup_message = self._read_popup_message()
                if popup_message:
                    screenshot_path = os.path.join('tests', 'screenshots', f"failed_{time.strftime('%Y%m%d_%H%M%S')}.png")
                    self.page.screenshot(path=screenshot_path)
                    logger.info(f'Error Message : {popup_message}')
                else:
                    popup_message = 'Unknown response after submit'
                    logger.warning(popup_message)

            if scenario == 'New':
                if member_id.startswith('MEMBER-') or 'MEMBER-' in popup_message:
                    return 'Saved'
                return popup_message

            if scenario == 'Duplicate':
                lowered = popup_message.lower()
                if member_id.startswith('MEMBER-') or 'member-' in lowered:
                    return 'DEFECT: Duplicate member was saved successfully - validation missing.'
                if 'exists' in lowered or 'duplicate' in lowered or 'already exists' in lowered:
                    return 'This member already exists'
                return popup_message

            return 'Invalid Scenario'

        except Exception as e:
            traceback.print_exc()
            return f'Exception: {str(e)}'
