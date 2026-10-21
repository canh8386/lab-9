"""Seven independent Selenium UI tests for the public SauceDemo test site."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


BASE_URL = "https://www.saucedemo.com/"


def login(driver, wait, username="standard_user", password="secret_sauce"):
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def login_successfully(driver, wait):
    login(driver, wait)
    wait.until(EC.url_contains("inventory.html"))
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"


def add_backpack(driver, wait):
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()


def test_tc01_login_success(driver, wait):
    login_successfully(driver, wait)
    assert "inventory.html" in driver.current_url


def test_tc02_login_wrong_password(driver, wait):
    login(driver, wait, password="incorrect_password")
    error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test="error"]')))
    assert "Username and password do not match" in error.text
    assert "inventory.html" not in driver.current_url


def test_tc03_add_to_cart(driver, wait):
    login_successfully(driver, wait)
    add_backpack(driver, wait)
    badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert badge.text == "1"
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))).text == "Sauce Labs Backpack"


def test_tc04_remove_from_cart(driver, wait):
    login_successfully(driver, wait)
    add_backpack(driver, wait)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait.until(EC.element_to_be_clickable((By.ID, "remove-sauce-labs-backpack"))).click()
    assert len(driver.find_elements(By.CLASS_NAME, "cart_item")) == 0
    assert len(driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")) == 0


def test_tc05_sort_price_low_to_high(driver, wait):
    login_successfully(driver, wait)
    Select(wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))).select_by_value("lohi")
    wait.until(lambda d: d.find_element(By.CLASS_NAME, "product_sort_container").get_attribute("value") == "lohi")
    prices = [float(el.text.replace("$", "")) for el in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
    assert len(prices) > 1
    assert prices == sorted(prices)



def test_tc06_checkout_success(driver, wait):
    login_successfully(driver, wait)
    add_backpack(driver, wait)

    # Mo gio hang va bat dau thanh toan
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # Nhap thong tin khach hang
    wait.until(EC.visibility_of_element_located(
        (By.ID, "first-name")
    )).send_keys("Test")

    driver.find_element(By.ID, "last-name").send_keys("Student")
    postal_code = driver.find_element(By.ID, "postal-code")
    postal_code.send_keys("10000")
    if postal_code.get_attribute("value") != "10000":
        driver.execute_script(
            """
            const input = arguments[0];
            const setter = Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype, 'value'
            ).set;
            setter.call(input, arguments[1]);
            input.dispatchEvent(new Event('input', {bubbles: true}));
            input.dispatchEvent(new Event('change', {bubbles: true}));
            """,
            postal_code,
            "10000",
        )

    # Kiem tra thong tin truoc khi tiep tuc
    assert driver.find_element(By.ID, "first-name").get_attribute("value") == "Test"
    assert driver.find_element(By.ID, "last-name").get_attribute("value") == "Student"
    assert postal_code.get_attribute("value") == "10000"

    continue_button = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
    driver.execute_script("arguments[0].click();", continue_button)

    # Kiem tra trang sau khi nhan Continue
    try:
        wait.until(EC.url_contains("checkout-step-two.html"))
    except Exception:
        print("\nURL hien tai:", driver.current_url)
        errors = driver.find_elements(By.CSS_SELECTOR, '[data-test="error"]')
        for error in errors:
            print("Thong bao loi:", error.text)
        driver.save_screenshot("tc06_error.png")
        raise

    # Hoan tat don hang
    finish_button = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
    driver.execute_script("arguments[0].click();", finish_button)

    message = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )

    assert message.text == "Thank you for your order!"
    assert "checkout-complete.html" in driver.current_url



def test_tc07_logout(driver, wait):
    login_successfully(driver, wait)
    menu_button = wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
    driver.execute_script("arguments[0].click();", menu_button)
    logout_link = wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
    driver.execute_script("arguments[0].click();", logout_link)
    assert wait.until(EC.visibility_of_element_located((By.ID, "login-button"))).is_displayed()
    assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")
