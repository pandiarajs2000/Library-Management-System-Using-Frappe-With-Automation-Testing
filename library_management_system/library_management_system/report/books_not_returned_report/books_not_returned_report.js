// Copyright (c) 2025, Pandiaraj and contributors
// For license information, please see license.txt

frappe.query_reports["Books Not Returned Report"] = {
	"filters": [
		{
			"fieldname":"member",
			"fieldtype":"Link",
			"options":"Library Member",
			"label":"Member ID"
		},
		{
			"fieldname":"book",
			"fieldtype":"Link",
			"options":"Book Details",
			"label":"Book ID"
		},
		{
			"fieldname":"author",
			"fieldtype":"Link",
			"options":"Authors",
			"label":"Author Name"
		},
	]
};
