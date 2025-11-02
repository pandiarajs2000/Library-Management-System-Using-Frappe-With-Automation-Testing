# Copyright (c) 2025, Pandiaraj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from frappe.utils import today


class LibraryTransaction(Document):
    def before_save(self):
        frappe.log_error("Doc", self.issue_or_return)
        if self.issue_or_return == "Issue":
            settings_data = frappe.get_single("Library Settings")
            frappe.log_error("Settsings", settings_data)
            count = frappe.db.count("Library Transaction", 
                                    {
                                        "member":self.member,
                                        "issue_or_return":self.issue_or_return,
                                        "return_date":['is', 'not set']
                                    }
                                    )
            frappe.log_error("Count", count)
            if count >= settings_data.maximum_limit:
                frappe.throw(f"Member {self.member} has reached the limit.")
            book = frappe.get_doc('Book Details', self.book)
            if book.available_copies <=0:
                frappe.throw(f"No Available copies for the book: {book.book_title}")
            book.available_copies -= 1
            book.save()
        # if self.issue_or_return == "Return":
        #         book = frappe.get_doc("Book Details", self.book)
        #         book.available_copies += 1
        #         book.save()
        #         if self.return_date and self.due_date and self.return_date > self.due_date:
        #             settings = frappe.get_single("Library Settings")
        #             days_late = (self.return_date - self.due_date).days
        #             self.penalty = days_late * settings.penalty_per_day
        

@frappe.whitelist()
def make_return_entry(source_name):
    """Create a Return entry from an issued transaction."""
    source_doc = frappe.get_doc("Library Transaction", source_name)
    
    if source_doc.issue_or_return != "Issue":
        frappe.throw("You can only return an issued book.")

    new_doc = frappe.new_doc("Library Transaction")
    new_doc.issue_or_return = "Return"
    new_doc.member = source_doc.member
    new_doc.book = source_doc.book
    new_doc.issue_date = source_doc.issue_date
    new_doc.due_date = source_doc.due_date
    new_doc.return_date = today()

    if source_doc.due_date and getdate(new_doc.return_date) > getdate(source_doc.due_date):
        settings = frappe.get_single("Library Settings")
        days_late = (getdate(new_doc.return_date) - getdate(source_doc.due_date)).days
        new_doc.penalty = days_late * settings.penalty_per_day

    book = frappe.get_doc("Book Details", source_doc.book)
    book.available_copies += 1
    book.save(ignore_permissions=True)

    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    frappe.msgprint(f"Book '{book.book_title}' returned successfully.")
    return new_doc