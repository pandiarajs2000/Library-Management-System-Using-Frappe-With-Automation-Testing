# import openpyxl
# def read_data(file_path, sheet_name, row, column):
#     wb = openpyxl.load_workbook(file_path)
#     sheet = wb[sheet_name]
#     return sheet.cell(row=row, column=column).value

# def write_data(file_path, sheet_name, row, column, data):
#     # Load the existing workbook
#     workbook = openpyxl.load_workbook(file_path)
#     if sheet_name in workbook.sheetnames:
#         worksheet = workbook[sheet_name]
#     else:
#         raise ValueError(f"Sheet '{sheet_name}' not found in the workbook.")
#     worksheet.cell(row=row, column=column, value=data)
#     workbook.save(file_path)

# def read_data_from_excel(file_path, sheet_name):
#     workbook = openpyxl.load_workbook(file_path)
#     sheet = workbook[sheet_name]

#     # fetch the first row as header
#     headers = [cell.value for cell in sheet[1]]
    
#     print(headers)

#     # fetch the data
#     data_list = []

#     for data in sheet.iter_rows(min_row=2, values_only=True):
#         row_dict = dict(zip(headers, data))
#         data_list.append(row_dict)
#     return data_list

import json

def load_test_data():
    with open("test_data/test_library_member.json") as file:
        data = json.load(file)
    return data

def get_login_data():
    data = load_test_data()
    return data["login"]

def get_library_member_data():
    data = load_test_data()
    return data["library_member"]