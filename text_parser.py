import time
import keyboard
import pyautogui
import pyperclip
import re

PHONE_PATTERN = r"מספר טלפון ראשי:\s*(\d{2,3}-?\d{6,7})"
CLIENT_ID_PATTERN = r"בעל הכרטיס זיהוי הלקוח:\s*(\d+)"

def extract_main_phone_number_and_address():
    text = _copy_page_text()

    phone_number = _extract_phone_number(text)
    address = _safe_extract_address(text)
    client_id = _extract_client_id(text)

    if address:
        print("🏠 Найден адрес:", address)
    else:
        print("❌ Адрес не найден.")

    return phone_number, address, client_id 

def _extract_client_id(text):
    match = re.search(CLIENT_ID_PATTERN, text)
    if match:
        client_id = match.group(1)
        print("🆔 Найден идентификатор клиента:", client_id)
        return client_id
    print("❌ Идентификатор клиента не найден.")
    return None

def _copy_page_text():
    time.sleep(0.3)
    pyautogui.click(x=1000, y=400)
    time.sleep(0.3)
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.3)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.3)
    return pyperclip.paste()


def _extract_phone_number(text):
    match = re.search(PHONE_PATTERN, text)
    if match:
        phone_number = match.group(1).replace("-", "")
        print("📞 Найден номер:", phone_number)
        return phone_number
    print("❌ Номер не найден.")
    return None


def _safe_extract_address(text):
    try:
        lines = text.splitlines()
        return _extract_address_from_lines(lines)
    except Exception as e:
        print(f"⚠️ Ошибка при извлечении адреса: {e}")
        return ""


def _extract_address_from_lines(lines):
    block_index = _find_address_block(lines)
    if block_index == -1:
        return ""

    shinui_index = _find_shinui_index(lines, block_index)
    if shinui_index == -1:
        return ""

    return _extract_address(lines, shinui_index)


def _find_address_block(lines):
    for i, line in enumerate(lines):
        print(f"[LOG] Проверка строки {i}: {line}")
        if "איש קשר לחיוב" in line:
            print(f"✅ Найден блок 'איש קשר לחיוב' в строке {i}")
            return i
    return -1


def _find_shinui_index(lines, start):
    for j in range(start + 1, len(lines)):
        print(f"[LOG] Поиск 'שינוי' — строка {j}: {lines[j]}")
        if "שינוי" in lines[j]:
            print(f"✅ Найден 'שינוי' в строке {j}")
            return j
    return -1


def _extract_address(lines, start):
    addr_lines = []
    for k in range(start + 1, len(lines)):
        l = lines[k].strip()
        print(f"[LOG] Кандидат в адрес — строка {k}: '{l}'")

        if not l:
            continue
        if any(kw in l for kw in ["שינוי", "איש קשר"]):
            continue
        if not any(char.isdigit() for char in l):
            print(f"⛔ Пропущено как имя (нет цифр): '{l}'")
            continue

        addr_lines.append(l)
        if len(addr_lines) >= 2:
            break

    print(f"📦 Адресные строки: {addr_lines}")
    return " ".join(addr_lines)
