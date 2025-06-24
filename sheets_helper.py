import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Access setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("דאטה נציגים - צוות אלירן").sheet1

# Get row by number (n)
def get_row(n):
    row = sheet.row_values(n)
    print(f"📥 Row {n} fetched: {row}")
    return row

def update_row(n, status=None, number=None, connect_line=None, disconnect_line=None, address=None, client_id=None):
    if status is not None:
        sheet.update_cell(n, 3, status)
    if number is not None:
        sheet.update_cell(n, 4, number)
    if connect_line is not None:
        sheet.update_cell(n, 6, connect_line)
    if disconnect_line is not None:
        sheet.update_cell(n, 5, disconnect_line)
    if address is not None:
        sheet.update_cell(n, 7, address)
    if client_id is not None:
        sheet.update_cell(n, 8, client_id)
    print(f"✅ Row {n} updated → Status: {status}, Number: {number}, Connect Line: {connect_line}, Disconnect Line: {disconnect_line}, Address: {address}, Client ID: {client_id}")