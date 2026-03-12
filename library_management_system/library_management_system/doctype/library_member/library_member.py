# Copyright (c) 2025, Pandiaraj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):
	def before_insert(self):
		if frappe.db.exists('Library Member', {'email': self.email}):
			frappe.throw('A library member with this email already exists.')