import time
import pyautogui
from buttons import click_first_button, click_home_button, click_nivut_button, click_on_image, click_show_canceled_checkbox, count_all_lines, fill_client_number_by_label_image, get_visible_lines_count
from pywinauto import Desktop, Application
from sheets_helper import get_row, update_row
from ui_helper import focus_and_click_center
pyautogui.FAILSAFE = False
import requests
import os
from dotenv import load_dotenv
from text_parser import extract_main_phone_number_and_address

load_dotenv()  # Load from .env

IMG_CLIENT_FOLDER = "png/client_folder_1.png"
IMG_CLIENT_LABEL = "png/client_label.png"
IMG_SEARCH_BUTTON = "png/search.png"
IMG_NIVUT_BUTTON = "png/nivut.png"
IMG_NIVUT_SECOND = "png/nivut2.png"
IMG_HOME_BUTTON = "png/home.png"
IMG_CHECKBOX_EMPTY = "png/checkbox_empty.png"

# === Text Constants ===
TITLE_MAIN_WINDOW = "Internet Explorer"
CONNECTED_STATUS_TEXT = "לקוח מחובר"

# === Row Range ===
ROW_NUM_START = 1193
ROW_NUM_END = 1252

def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("⛔ bot_token or chat_id not found in .env")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as err:
        print(f"⛔ Error sending message to Telegram: {err}")

if __name__ == "__main__":
    window_title = TITLE_MAIN_WINDOW
    app_window = focus_and_click_center(window_title)

    row_num_start = ROW_NUM_START
    row_num_end = ROW_NUM_END

    if app_window:
        current_row = row_num_start

        previous_num = ""
        flag = False
        while current_row <= row_num_end:
            print(f"\n📄 Processing row {current_row}...")

            try:
                row_data = get_row(current_row)

                client_code = row_data[0] if len(row_data) > 0 else ""
                client_name = row_data[1] if len(row_data) > 1 else ""

                print("👤 Client code:", client_code)
                print("👤 Client name:", client_name)

                click_on_image(IMG_CLIENT_FOLDER)
                time.sleep(1)
                fill_client_number_by_label_image(IMG_CLIENT_LABEL, client_code)
                time.sleep(0.5)
                click_first_button(IMG_SEARCH_BUTTON)

                time.sleep(1)
                number, address, client_id = extract_main_phone_number_and_address()

                if not number:
                    raise ValueError("❌ Failed to get phone number, retrying iteration...")

                if number == previous_num:
                    if not flag:
                        flag = True
                        print("🔁 Повтор номера — пробуем заново.")
                        raise ValueError("❌ Повтор номера — пробуем заново.")
                    else:
                        print("⚠️ Повтор снова — пропускаем строку.")
                        flag = False
                        current_row += 1
                        continue
                else:
                    flag = False
                    previous_num = number

                time.sleep(1)
                click_nivut_button(IMG_NIVUT_SECOND)

                connect_line = get_visible_lines_count()

                print(f"Connect_line {connect_line}")

                if connect_line > 2:
                    status = CONNECTED_STATUS_TEXT
                else:
                    status = ""

                click_show_canceled_checkbox()
                time.sleep(0.5)
                all_lines = count_all_lines()
                print(f"⚠️ total_after {all_lines}")
                disconnect_line = all_lines - connect_line

                time.sleep(0.7)
                click_nivut_button(IMG_NIVUT_BUTTON)
                time.sleep(0.6)
                click_home_button(IMG_HOME_BUTTON)

                update_row( current_row, status=status, number=number, connect_line=connect_line , disconnect_line=disconnect_line , address=address, client_id=client_id )

                number  = None
                address = None
                client_id = None
                current_row += 1

            except Exception as e:
                print(f"⚠️ Error processing row {current_row}, trying again...\n{e}")
                click_home_button(IMG_HOME_BUTTON)  # 🏠 Try to return the interface to its initial state
                time.sleep(1)
                click_nivut_button(IMG_NIVUT_BUTTON)
                time.sleep(1)
                click_home_button(IMG_HOME_BUTTON)
    else:
        print("⛔ Failed to get window, stopping script.")
