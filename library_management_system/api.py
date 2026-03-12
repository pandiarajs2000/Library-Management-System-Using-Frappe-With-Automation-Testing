import frappe

@frappe.whitelist()
def get_library_members():
    members = frappe.get_all('Library Member', fields=['member_name','email','phone','date_of_joined','status'])
    return members

@frappe.whitelist()
def create_library_member(member_name, email, phone, date_of_joined, status):
    if frappe.db.exists('Library Member', {'email': email}):
        frappe.throw('A library member with this email already exists.')
        return {
            "status": "Already Exists",
            "message": f"A library member with this {email} already exists."
        }

    member = frappe.get_doc({
        'doctype': 'Library Member',
        'member_name': member_name,
        'email': email,
        'phone': phone,
        'date_of_joined': date_of_joined,
        'status': status
    })
    frappe.log_error(f"Creating library member: {member_name}")
    member.insert()
    return {
        "status": "Success",
        "message": f"Library member {member_name} created successfully."
    }