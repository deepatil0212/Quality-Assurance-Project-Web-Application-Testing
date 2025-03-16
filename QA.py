from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  # Fix SSL errors
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

# ========================== TEST FUNCTIONS ==========================

def test_login():
    """Logs in to the SauceDemo website"""
    driver.get("https://www.saucedemo.com/")
    
    try:
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Username"))
        )
        password = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_button.click()

        WebDriverWait(driver, 10).until(EC.title_contains("Swag Labs"))
        print("✅ Login Test Passed!")
    except Exception as e:
        print("❌ Login Test Failed:", str(e))


def test_add_to_cart():
    """Adds a product to the cart"""
    try:
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        add_to_cart_button.click()
        
        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        print("✅ Add to Cart Test Passed!")
    except Exception as e:
        print("❌ Add to Cart Test Failed:", str(e))


def test_checkout():
    """Proceeds to checkout"""
    try:
        checkout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout"))
        )
        checkout_button.click()

        first_name = driver.find_element(By.ID, "first-name")
        last_name = driver.find_element(By.ID, "last-name")
        postal_code = driver.find_element(By.ID, "postal-code")

        first_name.send_keys("Deepa")
        last_name.send_keys("Patil")
        postal_code.send_keys("123456")

        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()

        finish_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "finish"))
        )
        finish_button.click()

        confirmation_message = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert "Thank you for your order!" in confirmation_message
        print("✅ Checkout Test Passed!")
    except Exception as e:
        print("❌ Checkout Test Failed:", str(e))

# ========================== EXECUTE TESTS ==========================

test_login()
test_add_to_cart()
test_checkout()

# Close the browser
time.sleep(3)
driver.quit()
