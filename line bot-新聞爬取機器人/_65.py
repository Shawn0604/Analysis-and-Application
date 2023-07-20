import os
from Google import Create_Service

FOLDER_PATH = r'.credentials'
CLIENT_SECRET_FILE = os.path.join(FOLDER_PATH,'client_secret.json')
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)


import os
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

spreadsheet_id = '1SThj-wFLlDVXfLcRCdaDLYGcO3Tj1zfCN4ogepklNoY'
mySpreadsheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

"""
values.pdate method
"""
worksheet_name = 'Sales North!'
cell_range_insert = 'B2:C4'
values = (
    ('Col A', 'Col B', 'Col C', 'Col D'),
    ('Apple', 'Orange', 'Watermelon', 'Banana')
)
value_range_body = {
    'majorDimension': 'ROWS',
    'values': values
}

# service.spreadsheets().values().update(
#     spreadsheetId=spreadsheet_id,
#     valueInputOption='USER_ENTERED',
#     range=worksheet_name + cell_range_insert,
#     body=value_range_body
# ).execute()



# service.spreadsheets().values().clear(
#     spreadsheetId=spreadsheet_id,
#     range='Sales North'
# ).execute()


# worksheet_name = 'Sales North!'
# cell_range_insert = 'B2:E3'
# values = (
#     ('Col A', 'Col B', 'Col C', 'Col D'),
#     ('Apple', 'Orange', 'Watermelon', 'Banana')
# )
# value_range_body = {
#     'majorDimension': 'COLUMNS',
#     'values': values
# }
#
# service.spreadsheets().values().update(
#     spreadsheetId=spreadsheet_id,
#     valueInputOption='USER_ENTERED',
#     range=worksheet_name + cell_range_insert,
#     body=value_range_body
# ).execute()


"""
values.append
"""

worksheet_name = 'Sales North!'
cell_range_insert = 'B2'
values = (
    ('Col E', 'Col F', 'Col G', 'Col H'),
    ('Toyota', 'Honda', 'Tesla', 'BMW')
)
value_range_body = {
    'majorDimension': 'COLUMNS',
    'values': values
}

service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    valueInputOption='USER_ENTERED',
    range=worksheet_name + cell_range_insert,
    body=value_range_body
).execute()

# for(i=0;i<5;i++){
# 　document.write(i);
# }