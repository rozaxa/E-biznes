import time
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_basic_auth_wrong_password():
    url_with_credentials = "https://student:ebiznes@the-internet.herokuapp.com/basic_auth"
    driver = webdriver.Chrome()
    driver.get(url_with_credentials)
    content = driver.find_element(By.TAG_NAME, "body").text
    assert "Congratulations!" not in content

def test_drag_and_drop():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/drag_and_drop")
    box_a = driver.find_element(By.ID, "column-a")
    box_b = driver.find_element(By.ID, "column-b")
    ActionChains(driver).drag_and_drop(box_a, box_b).perform()
    assert box_a.text == 'B' and box_b.text == 'A'

def test_drag_and_drop_second():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/drag_and_drop")
    box_a = driver.find_element(By.ID, "column-a")
    box_b = driver.find_element(By.ID, "column-b")
    ActionChains(driver).drag_and_drop(box_a, box_a).perform()
    assert box_a.text == 'A' and box_b.text != 'A'


def test_dropdown():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 2")
    selected_option = dropdown.first_selected_option
    assert selected_option.text == "Option 2"

def test_dropdown():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 1")
    selected_option = dropdown.first_selected_option
    assert selected_option.text != "Option 2"


def test_notification_message(driver):
    driver.get("https://the-internet.herokuapp.com/notification_message_rendered")
    driver.find_element(By.LINK_TEXT, "Click here").click()
    message = driver.find_element(By.ID, "flash").text
    assert "Action successful" in message or "Action unsuccesful, please try again" in message

def test_floating_menu_visibility(driver):

    driver.get("https://the-internet.herokuapp.com/floating_menu")
    menu = driver.find_element(By.ID, "menu")
    assert menu.is_displayed()
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.END)
    assert menu.is_displayed()

def test_slider_movement(driver):
    driver.get("https://the-internet.herokuapp.com/horizontal_slider")
    slider = driver.find_element(By.CSS_SELECTOR, "input[type='range']")
    for _ in range(10):
        slider.send_keys(Keys.ARROW_LEFT)

    slider.send_keys(Keys.ARROW_RIGHT)

    slider_value = driver.find_element(By.ID, "range").text
    assert slider_value == "0.5"
    slider.send_keys(Keys.ARROW_LEFT)
    slider_value = driver.find_element(By.ID, "range").text

def test_infinite_scroll(driver):
    driver.get("https://the-internet.herokuapp.com/infinite_scroll")
    body = driver.find_element(By.TAG_NAME, "body")
    paragraphs_before_scroll = len(driver.find_elements(By.CLASS_NAME, "jscroll-added"))

    for _ in range(3):
        body.send_keys(Keys.END)
        time.sleep(2)

    paragraphs_after_scroll = len(driver.find_elements(By.CLASS_NAME, "jscroll-added"))
    assert paragraphs_after_scroll > paragraphs_before_scroll


def test_nested_frames(driver):
    driver.get("https://the-internet.herokuapp.com/nested_frames")

    driver.switch_to.frame("frame-top")
    driver.switch_to.frame("frame-left")
    left_frame_text = driver.find_element(By.TAG_NAME, "body").text
    assert left_frame_text == "LEFT"

    driver.switch_to.parent_frame()
    driver.switch_to.frame("frame-middle")
    middle_frame_text = driver.find_element(By.TAG_NAME, "body").text
    assert middle_frame_text == "MIDDLE"

    driver.switch_to.parent_frame()
    driver.switch_to.frame("frame-right")
    right_frame_text = driver.find_element(By.TAG_NAME, "body").text
    assert right_frame_text == "RIGHT"

    driver.switch_to.default_content()
    driver.switch_to.frame("frame-bottom")
    bottom_frame_text = driver.find_element(By.TAG_NAME, "body").text
    assert bottom_frame_text == "BOTTOM"

def test_multiple_windows(driver):
    driver.get("https://the-internet.herokuapp.com/windows")
    original_window = driver.current_window_handle
    link = driver.find_element(By.LINK_TEXT, "Click Here")
    link.click()

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    header_text = driver.find_element(By.TAG_NAME, "h3").text
    assert header_text == "New Window"
    driver.close()
    driver.switch_to.window(original_window)
    driver.quit()







