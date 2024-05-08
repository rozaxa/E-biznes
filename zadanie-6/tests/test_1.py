import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_title(driver):
    driver.get("https://the-internet.herokuapp.com/")
    assert "The Internet" in driver.title


def test_title_new(driver):
    driver.get("https://the-internet.herokuapp.com/")
    assert "Ebiznes" not in driver.title


def test_ab_test_text(driver):
    driver.get("https://the-internet.herokuapp.com/abtest")
    actual_text = driver.find_element(By.CSS_SELECTOR, ".example > p").text
    expected_phrases = [
        "Also known as split testing",
        "businesses are able to simultaneously test and learn different versions of a page",
        "see which text and/or functionality works best"
    ]
    assert all(phrase in actual_text for phrase in expected_phrases)

def test_add_elements(driver):
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")
    for _ in range(3):
        add_button.click()
    delete_buttons = driver.find_elements(By.CLASS_NAME, 'added-manually')
    assert len(delete_buttons) == 3

def test_remove_elements(driver):
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")
    add_button.click()
    delete_button = driver.find_element(By.CLASS_NAME, 'added-manually')
    delete_button.click()
    delete_buttons = driver.find_elements(By.CLASS_NAME, 'added-manually')
    assert len(delete_buttons) == 0

def test_add_and_remove_multiple_elements(driver):
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")
    for _ in range(5):
        add_button.click()
    delete_buttons = driver.find_elements(By.CLASS_NAME, 'added-manually')
    while delete_buttons:
        delete_buttons[0].click()
        delete_buttons = driver.find_elements(By.CLASS_NAME, 'added-manually')
    assert len(delete_buttons) == 0

def test_broken_images(driver):
    driver.get("https://the-internet.herokuapp.com/broken_images")
    images = driver.find_elements(By.TAG_NAME, "img")
    broken_images_count = 0
    for image in images:
        if image.get_attribute('naturalWidth') == "0":
            print(f"Broken image found: {image.get_attribute('src')}")
            broken_images_count += 1
    assert broken_images_count != 0

def test_checkboxes_toggle(driver):
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
            assert checkbox.is_selected()
        else:
            checkbox.click()
            assert not checkbox.is_selected()

def test_initial_state_of_checkboxes(driver):
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    assert not checkboxes[0].is_selected()
    assert checkboxes[1].is_selected()

def test_basic_auth():
    url_with_credentials = "https://admin:admin@the-internet.herokuapp.com/basic_auth"
    driver = webdriver.Chrome()
    driver.get(url_with_credentials)
    content = driver.find_element(By.TAG_NAME, "body").text
    assert "Congratulations!" in content, "Authentication failed or the wrong page content"





