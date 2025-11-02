// Copyright (c) 2025, Pandiaraj and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Transaction", {
	refresh(frm) {
        frm.add_custom_button(__('Return a Book'), function() {
           create_return(frm)
       }, __("Create"));
	},
});

function create_return(frm)
{
    console.log("Create",frm.doc.docstatus);
    
    if (frm.doc.docstatus == 1 && frm.doc.issue_or_return == "Issue") {
        frappe.call({
            method: "library_management_system.library_management_system.doctype.library_transaction.library_transaction.make_return_entry",
            args: { 'source_name': frm.doc.name },
            callback: function(r) {
                if (r.message) {
                    // frappe.model.sync(r.message);
                    // frappe.set_route("Form", r.message.doctype, r.message.name);/
                    console.log("message", r.message);
                }
            }
        });
    }
}