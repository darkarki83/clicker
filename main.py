import win32gui
import win32con
import time
import pyperclip
import re
import pyautogui
import keyboard
from pywinauto import Desktop, Application
from sheets_helper import get_row, update_row
pyautogui.FAILSAFE = False

def focus_and_click_center(window_title_part):
    windows = Desktop(backend="uia").windows()
    target_window = None

    for w in windows:
        if window_title_part in w.window_text():
            target_window = w
            break

    if not target_window:
        print("❌ Окно не найдено.")
        return None

    print("✅ Окно найдено!")

    try:
        hwnd = target_window.handle
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        time.sleep(0.5)
        win32gui.SetForegroundWindow(hwnd)
        print("📌 Окно выведено на передний план.")
        time.sleep(1)

        rect = target_window.rectangle()
        center_x = rect.left + rect.width() // 2
        center_y = rect.top + rect.height() // 2

        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        print("🖱️ Клик выполнен в центр окна.")
        return target_window

    except Exception as e:
        print("⚠️ Ошибка при попытке фокуса:", e)
        return None

def click_on_image(image_path, confidence=0.8, timeout=10):
    print(f"🔍 Ищем изображение: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=0.2)
            pyautogui.click()
            print(f"✅ Клик по изображению выполнен: {image_path}")
            return True
        time.sleep(0.5)

    print(f"❌ Изображение не найдено за {timeout} сек: {image_path}")
    return False

def fill_client_number_by_label_image(label_image_path, client_code="1234"):
    print("🧩 Ищем лейбл по изображению:", label_image_path)
    location = pyautogui.locateOnScreen(label_image_path, confidence=0.9)
    if location:
        label_x, label_y = pyautogui.center(location)
        print("✅ Лейбл найден по координатам:", label_x, label_y)

        # Input находится слева от label
        input_x = label_x - 200
        input_y = label_y

        pyautogui.click(input_x, input_y)
        time.sleep(0.3)
        pyautogui.write(client_code)
        print("✅ Код клиента вставлен рядом с лейблом.")
    else:
        print("❌ Лейбл не найден на экране.")

def click_first_button(image_path, confidence=0.9, timeout=10):
    print(f"🔍 Ищем первую кнопку по изображению: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            if locations:
                # Берем первую кнопку сверху
                first = sorted(locations, key=lambda loc: loc.top)[0]
                center = pyautogui.center(first)
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                print("✅ Клик по первой найденной кнопке выполнен.")
                return True
        except Exception as e:
            print(f"⚠️ Ошибка при поиске кнопок: {e}")
        time.sleep(0.5)

    print(f"❌ Кнопка не найдена за {timeout} сек.")
    return False

def minimize_popup_window(partial_title):
    print(f"🔍 Ищем всплывающее окно: '{partial_title}'")
    try:
        windows = Desktop(backend="uia").windows()
        for win in windows:
            if partial_title in win.window_text():
                win.minimize()
                print("✅ Всплывающее окно свернуто.")
                return True
        print("❌ Всплывающее окно не найдено.")
        return False
    except Exception as e:
        print("⚠️ Ошибка при сворачивании окна:", e)
        return False

def extract_main_phone_number():
    print("📋 Копируем текст со страницы...")

    # Можно кликнуть в координаты, где точно есть текст
    pyautogui.click(x=1000, y=500)  # Настрой координаты!
    time.sleep(0.5)

    # Теперь эмулируем ввод клавиш с помощью keyboard
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.5)

    # 🖱️ Кликнем ниже, чтобы снять выделение (на 100 пикселей вниз)
    current_x, current_y = pyautogui.position()
    pyautogui.click(current_x, current_y + 100)
    time.sleep(0.3)

    text = pyperclip.paste()
    print("📑 Текст получен:\n", text)

    match = re.search(r"מספר טלפון ראשי:\s*(\d{2,3}-?\d{6,7})", text)
    if match:
        phone_number = match.group(1).replace("-", "")
        print("📞 Найден номер:", phone_number)
        return phone_number
    else:
        print("❌ Номер не найден.")
        return None

def click_nivut_button(image_path="nivut.png", confidence=0.9, timeout=10):
    print(f"🧭 Ищем кнопку ניווט по изображению: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                print("✅ Клик по кнопке ניווט выполнен.")
                return True
        except Exception as e:
            print(f"⚠️ Ошибка при поиске кнопки ניווט: {e}")
        time.sleep(0.5)

    print(f"❌ Кнопка ניווט не найдена за {timeout} сек.")
    return False

def get_visible_lines_count():
    print("📋 Считаем количество видимых линий...")

    # Сфокусируем окно (можно настроить координаты)
    pyautogui.click(x=1000, y=400)
    time.sleep(0.4)

    # Копируем текст
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.4)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.4)

    # Снимаем выделение
    current_x, current_y = pyautogui.position()
    pyautogui.click(current_x, current_y + 100)
    time.sleep(0.3)

    # Извлекаем текст
    text = pyperclip.paste()
    phone_matches = re.findall(r'972\d{8,9}', text)
    print(f"🔢 Найдено {len(phone_matches)} линий.")
    return len(phone_matches)

def click_show_canceled_checkbox(image_path="checkbox_empty.png", confidence=0.9, timeout=10):
    print(f"🔍 Ищем чекбокс по изображению: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                print("☑️ Чекбокс нажат.")
                return True
        except Exception as e:
            print("⚠️ Ошибка при поиске чекбокса:", e)

        time.sleep(0.5)

    print("❌ Чекбокс не найден.")
    return False

def count_all_lines():
    print("📋 Считаем все уникальные линии (после чекбокса)...")

    pyautogui.click(x=1000, y=400)
    time.sleep(0.4)
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.4)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.4)
    current_x, current_y = pyautogui.position()
    pyautogui.click(current_x, current_y + 100)
    time.sleep(0.3)

    text = pyperclip.paste()
    phone_matches = re.findall(r'972\d{8,9}', text)

    unique_numbers = set(phone_matches)  # Убираем дубликаты
    print(f"📞 Уникальных линий найдено: {len(unique_numbers)}")
    return len(unique_numbers)

def click_home_button(image_path="home.png", confidence=0.9, timeout=10):
    print(f"🏠 Ищем кнопку בית по изображению: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                print("✅ Клик по кнопке בית выполнен.")
                return True
        except Exception as e:
            print(f"⚠️ Ошибка при поиске кнопки בית: {e}")
        time.sleep(0.5)

    print(f"❌ Кнопка בית не найдена за {timeout} сек.")
    return False

def connect_to_app_and_print(app_window):
    try:
        app = Application(backend="uia").connect(handle=app_window.handle)
        window = app.top_window()
        print("🧩 Структура элементов в окне:")
        window.print_control_identifiers(depth=5)
    except Exception as e:
        print(f"❌ Ошибка при подключении и выводе элементов: {e}")

if __name__ == "__main__":
    window_title = "ברוך הבא למרחב העבודה שלך"
    app_window = focus_and_click_center(window_title)

    row_num_start = 1442
    row_num_end = 1570

    if app_window:
        current_row = row_num_start
        while current_row <= row_num_end:
            print(f"\n📄 Обработка строки {current_row}...")

            try:
                row_data = get_row(current_row)

                client_code = row_data[0] if len(row_data) > 0 else ""
                client_name = row_data[1] if len(row_data) > 1 else ""

                print("👤 Код клиента:", client_code)
                print("👤 Имя клиента:", client_name)

                click_on_image("client_folder.png")
                time.sleep(2)
                fill_client_number_by_label_image("client_label.png", client_code)
                click_first_button("search.png")

                time.sleep(8)
                minimize_popup_window("360")
                #time.sleep(2)
                #focus_and_click_center("פרטי לקוח")
                number = extract_main_phone_number()
                time.sleep(1)
                click_nivut_button("nivut2.png")

                total_before = get_visible_lines_count()

                if total_before > 2:
                    status = "לקוח מחובר"
                    count = 0
                else:
                    click_show_canceled_checkbox()
                    time.sleep(2)
                    total_after = count_all_lines()
                    print(f"⚠️ total_after {total_after}")
                    count = total_after - total_before
                    status = ""

                time.sleep(1)
                click_nivut_button("nivut.png")
                time.sleep(1)
                click_home_button("home.png")

                count_value = 0 if count == 0 else f"{total_before}/{count}"
                update_row(current_row, status=status, number=number, count=count_value)

                current_row += 1  # ✅ Увеличиваем только если всё прошло успешно

            except Exception as e:
                print(f"⚠️ Ошибка при обработке строки {current_row}, пробуем ещё раз...\n{e}")
                minimize_popup_window("360")
                click_home_button("home.png")  # 🏠 Попытка вернуть интерфейс в исходное состояние
                time.sleep(3)
    else:
        print("⛔ Не удалось получить окно, остановка скрипта.")