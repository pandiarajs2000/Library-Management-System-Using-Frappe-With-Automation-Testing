import frappe

@frappe.whitelist()
def get_library_members():
    members = frappe.get_all('Library Member', fields=['member_name','email','phone','date_of_joined','status'])
    return members