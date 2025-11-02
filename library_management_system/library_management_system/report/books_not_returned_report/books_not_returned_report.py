# Copyright (c) 2025, Pandiaraj and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	column = [
		{
			"fieldname":"member",
			"fieldtype":"Link",
			"options":"Library Member",
			"label":"Member ID",
			"width":150
		},
		{
			"fieldname":"status",
			"fieldtype":"Select",
			"options":["Active","Inactive"],
			"label":"Member Status",
			"width":100
		},
		{
			"fieldname":"book",
			"fieldtype":"Link",
			"options":"Book Details",
			"label":"Book ID",
			"width":200
		},
		{
			"fieldname":"author",
			"fieldtype":"Link",
			"options":"Authors",
			"label":"Author Name",
			"width":200
		},
		{
			"fieldname":"transaction_status",
			"fieldtype":"Select",
			"options":["Issue","Return"],
			"label":"Transaction Status",
			"width":100
		},
	]
	return column

def get_data(filters):
	conditions = ""

	if filters.get('member'):
		conditions += f"AND {filters.get('member')} = LM.member_name"
	if filters.get('book'):
		conditions += f"AND {filters.get('book')} = BD.book_title"
	if filters.get('author'):
		conditions += f"AND {filters.get('author')} = A.author_name"
	
	query = """
				SELECT
					LM.member_name AS member,
					LM.status AS status,
					BD.book_title AS book,
					A.author_name AS author,
					LT.issue_or_return AS transaction_status
				FROM `tabLibrary Transaction` AS LT
				INNER JOIN `tabLibrary Member` AS LM ON LM.name = LT.member
				INNER JOIN `tabBook Details` AS BD ON BD.name = LT.book
				INNER JOIN `tabAuthors` AS A ON A.name = BD.author_name
				WHERE LT.issue_or_return != "Return"
			"""
	
	execute_query = frappe.db.sql(query,as_dict=1)
	frappe.log_error("result",execute_query)
	return execute_query