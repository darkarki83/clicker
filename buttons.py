import time, pyautogui, pyperclip, keyboard, re

IMG_NIVUT_BUTTON = "png/nivut.png"
IMG_CHECKBOX_EMPTY = "png/checkbox_empty.png"
IMG_HOME_BUTTON = "png/home.png"

def click_on_image(image_path, confidence=0.8, timeout=10):
    print(f"🔍 Searching for image: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=0.2)
            pyautogui.click()
            print(f"✅ Click on image performed: {image_path}")
            return True
        time.sleep(0.3)

    print(f"❌ Image not found within {timeout} seconds: {image_path}")
    return False

def fill_client_number_by_label_image(label_image_path, client_code="1234"):
    print("🧩 Searching for label by image:", label_image_path)
    location = pyautogui.locateOnScreen(label_image_path, confidence=0.9)
    if location:
        label_x, label_y = pyautogui.center(location)
        # Input is to the left of the label
        input_x = label_x - 200
        input_y = label_y

        pyautogui.click(input_x, input_y)
        time.sleep(0.3)
        pyautogui.write(client_code)
    else:
        print("❌ Label not found on the screen.")
        
def click_first_button(image_path, confidence=0.9, timeout=10):
    print(f"🔍 Searching for the first button by image: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            if locations:
                # Take the first button from the top
                first = sorted(locations, key=lambda loc: loc.top)[0]
                center = pyautogui.center(first)
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                return True
        except Exception as e:
            print(f"⚠️ Error while searching for buttons: {e}")
        time.sleep(0.5)

    print(f"❌ Button not found within {timeout} seconds.")
    return False

def click_nivut_button(image_path=IMG_NIVUT_BUTTON, confidence=0.9, timeout=5):
    print(f"🧭 Searching for the navigation button by image: {image_path}")
    attempts = 0
    while attempts < 3:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                return True
            else:
                print(f"🔄 Navigation button not found. Retry {attempts + 1}/3")
                time.sleep(1)
                attempts += 1
        except Exception as e:
            print(f"⚠️ Error while searching for navigation button: {e}")
            attempts += 1
    print("❌ Failed to click on the navigation button after 3 attempts.")
    return False

def click_home_button(image_path=IMG_HOME_BUTTON, confidence=0.9, timeout=10):
    print(f"🏠 Searching for home button by image: {image_path}")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                print("✅ Click on home button performed.")
                return True
        except Exception as e:
            print(f"⚠️ Error while searching for home button: {e}")
        time.sleep(0.4)

    print(f"❌ Home button not found within {timeout} seconds.")
    return False

def click_show_canceled_checkbox(image_path=IMG_CHECKBOX_EMPTY, confidence=0.9, timeout=3):
    print(f"🔍 Searching for checkbox by image: {image_path}")
    start_time = time.time()
    attempts = 0

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                print(f"📍 Checkbox found at coordinates: {center}")
                pyautogui.moveTo(center.x, center.y, duration=0.2)
                pyautogui.click()
                time.sleep(1)  # Wait to ensure UI has updated

                # 🔁 Check if checkbox is gone (meaning it was clicked)
                if not pyautogui.locateOnScreen(image_path, confidence=confidence):
                    return True
                else:
                    print("↩️ Trying to click again...")
                    attempts += 1
                    if attempts >= 3:
                        print("❌ Failed to click on the checkbox after 3 attempts.")
                        return False
        except Exception as e:
            print("⚠️ Error while searching for checkbox:", e)

        time.sleep(0.5)

    print("❌ Checkbox not found.")
    return False

def get_visible_lines_count():
    print("📋 Counting the number of visible lines...")

    # Focus the window (adjust coordinates as needed)
    pyautogui.click(x=1000, y=400)
    time.sleep(0.4)

    # Copy text
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.4)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.4)

    # Remove selection
    current_x, current_y = pyautogui.position()
    pyautogui.click(current_x, current_y + 100)
    time.sleep(0.3)

    # Extract text
    text = pyperclip.paste()
    phone_matches = re.findall(r'972\d{8,9}', text)
    print(f"🔢 Found {len(phone_matches)} lines.")
    return len(phone_matches)

def count_all_lines():
    print("📋 Counting all unique lines (after checkbox)...")

    pyautogui.click(x=1000, y=400)
    time.sleep(0.3)
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.3)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.3)
    current_x, current_y = pyautogui.position()
    pyautogui.click(current_x, current_y + 100)
    time.sleep(0.3)

    text = pyperclip.paste()
    phone_matches = re.findall(r'972\d{8,9}', text)

    unique_numbers = set(phone_matches)  # Убираем дубликаты
    print(f"📞 Found {len(unique_numbers)} unique lines.")
    return len(unique_numbers)