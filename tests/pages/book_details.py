from playwright.sync_api import Page, expect
from utils.logger_config import logger
from datetime import datetime, timedelta
import traceback
import time

class BookDetails:
    def __init__(self, page: Page):
        self.page = page
        self.book_title_xpath = "//div[@data-fieldname='book_title']//input[@type='text']"
        self.author_name_xpath = "//div[@data-fieldname='author_name']//input[@type='text']"
        self.publisher_name_xpath = "//div[@data-fieldname='publisher_name']//input[@type='text']"
        self.book_category_xpath = "//div[@data-fieldname='category']//input[@type='text']"
        self.isbn_xpath = "//div[@data-fieldname='isbn_number']//input[@type='text']"
        self.total_copies_xpath = "//div[@data-fieldname='total_copies']//input[@type='text']"
        self.available_copies_xpath = "//div[@data-fieldname='available_copies']//input[@type='text']"
        self.save_btn_xpath = "//button[@data-label='Save']"
        self.search_box_xpath = "//input[@id='navbar-search']"
        self.add_library_member = "//button[@data-label='Add Book Details']"
        self.member_id_xpath = "//li[@class='disabled']//a[starts-with(text(), 'LIB-')]"
        self.error_popup_xpath = "//div[@class='msgprint']"
    
    def validate_book_details_screen(self, book_title, author_name, publisher_name, book_category, isbn, total_copy, available_copy):
        try:
            logger.info("Search the Library Member List")
            search_input = self.page.locator(self.search_box_xpath)
            search_input.fill("Book Details")
            search_input.press("ArrowDown")
            self.page.wait_for_timeout(500)
            search_input.press("Enter")

            logger.info("Click the Add New Libary Member Button")
            add_new_btn = self.page.locator(self.add_library_member)
            add_new_btn.click()

            logger.info("Attempting the Library Member Page")
            book_title = str(book_title or "").strip()
            author_name = str(author_name or "").strip()
            publisher_name = str(publisher_name or "")
            book_category = str(book_category or "").strip()
            isbn = str(isbn or "").strip()
            total_copy = int(total_copy or "")
            available_copy = int(available_copy or "")
            
            
            book_title_input = self.page.locator(self.book_title_xpath)
            book_title_input.clear()
            book_title_input.fill(book_title)

            author_name_input = self.page.locator(self.author_name_xpath)
            author_name_input.clear()
            author_name_input.fill(author_name)
            
            publisher_name_input = self.page.locator(self.publisher_name_xpath)
            publisher_name_input.clear()
            publisher_name_input.fill(publisher_name)
            
            book_category_input = self.page.locator(self.book_category_xpath)
            book_category_input.clear()
            book_category_input.fill(book_category)
            
            isbn_input = self.page.locator(self.isbn_xpath)
            isbn_input.clear()
            isbn_input.fill(isbn)
            
            total_copy_input = self.page.locator(self.total_copies_xpath)
            total_copy_input.clear()
            total_copy_input.fill(total_copy)

            available_copy_input = self.page.locator(self.available_copies_xpath)
            available_copy_input.clear()
            available_copy_input.fill(available_copy)

            save_btn = self.page.locator(self.save_btn_xpath)
            save_btn.click()

        except Exception as e:
            raise e