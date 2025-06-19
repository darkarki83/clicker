import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройка доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("דאטה נציגים - צוות אלירן").sheet1

# Получение строки по номеру (n)
def get_row(n):
    row = sheet.row_values(n)
    print(f"📥 Получена строка {n}: {row}")
    return row

# Обновление строки (n) по колонкам: Статус (3), 25939582 (4), כמות קווים (5)
def update_row(n, status=None, number=None, count=None, address=None):
    if status is not None:
        sheet.update_cell(n, 3, status)
    if number is not None:
        sheet.update_cell(n, 4, number)
    if count is not None:
        sheet.update_cell(n, 5, count)
    if address is not None:
        sheet.update_cell(n, 6, address)
    print(f"✅ Обновлена строка {n} → Статус: {status}, Номер: {number}, Кол-во: {count}, Адрес: {address}")