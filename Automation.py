from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Constants
URL = "https://ecspro-qa.kloudship.com"
USERNAME = "kloudship.qa.automation@mailinator.com"
PASSWORD = "Password1"
PACKAGE_NAME = "Rhythm_gautam"
PACKAGE_DIMENSION = str(random.randint(1, 19))

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Color Codes for Print Output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def print_separator():
    print(CYAN + "-" * 60 + RESET)

def login():
    print_separator()
    print(YELLOW + "[🔐] Logging in..." + RESET)
    driver.get(URL)
    wait.until(EC.presence_of_element_located((By.ID, "login-email"))).send_keys(USERNAME)
    driver.find_element(By.ID, "login-password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@id='login-btn']").click()
    print(GREEN + "[✅] Successfully logged in!" + RESET)

def logout():
    print_separator()
    print(YELLOW + "[🚪] Logging out..." + RESET)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mat-focus-indicator mat-menu-trigger mat-tooltip-trigger mat-icon-button mat-button-base']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mat-focus-indicator mat-menu-item ng-tns-c99-1']"))).click()
    print(GREEN + "[✅] Successfully logged out!" + RESET)

def add_package():
    print_separator()
    print(YELLOW + f"[📦] Adding package: {PACKAGE_NAME} (Size: {PACKAGE_DIMENSION}x{PACKAGE_DIMENSION}x{PACKAGE_DIMENSION})..." + RESET)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='row count-card-wrapper'] mat-card:nth-child(8)"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mat-focus-indicator button-disabled mat-icon-button mat-button-base ng-star-inserted']//span[@class='mat-button-wrapper']"))).click()
    
    driver.find_element(By.XPATH, "//input[@formcontrolname='name']").send_keys(PACKAGE_NAME)
    driver.find_element(By.XPATH, "//input[@id='mat-input-3']").send_keys(PACKAGE_DIMENSION)
    driver.find_element(By.XPATH, "//input[@id='mat-input-4']").send_keys(PACKAGE_DIMENSION)
    driver.find_element(By.XPATH, "//input[@id='mat-input-5']").send_keys(PACKAGE_DIMENSION)
    
    driver.find_element(By.XPATH, "//mat-icon[@class='mat-icon notranslate material-icons mat-ligature-font mat-icon-no-color'][normalize-space()='check']").click()
    time.sleep(2)  # Allowing time for the package to be added
    print(GREEN + "[✅] Package added successfully!" + RESET)

def verify_package_exists():
    print_separator()
    print(YELLOW + f"[🔍] Verifying if package '{PACKAGE_NAME}' exists...")
    driver.get(URL)
    
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Ensure page loads
    
    login()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='row count-card-wrapper'] mat-card:nth-child(8)"))).click()

    # Wait for the package list to appear
    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='padding list-text'][contains(normalize-space(),'{PACKAGE_NAME}')]")))

    # Find the package
    packages = driver.find_elements(By.XPATH, f"//div[@class='padding list-text'][contains(normalize-space(),'{PACKAGE_NAME}')]")

    if packages:
        print(GREEN + f"[✅] Package '{PACKAGE_NAME}' found in the system!" + RESET)
    else:
        print(RED + "[❌] Package not found! Possible issues:" + RESET)
        print(RED + "- Package was never created." + RESET)
        print(RED + "- Page didn't load properly." + RESET)
        print(RED + "- XPath is incorrect or changed." + RESET)
        driver.save_screenshot("package_not_found.png")  # Save screenshot for debugging
        raise Exception("Newly created package not found!")

def delete_package():
    print_separator()
    print(YELLOW + f"[🗑️] Deleting package '{PACKAGE_NAME}'..." + RESET)

    package_row = wait.until(EC.presence_of_element_located((By.XPATH, f"(//div[@class='padding list-text'][contains(text(),'{PACKAGE_NAME}')])[1]")))

    actions = ActionChains(driver)
    actions.move_to_element(package_row).perform()
    print(GREEN + "   [✅] Hovered over the package." + RESET)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@appdialog='alert']//mat-icon[text()='delete']"))).click()
    print(GREEN + "   [✅] Clicked on delete button." + RESET)
    
    confirm_delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(),'Delete Package Type')]]")))
    confirm_delete_button.click()
    print(GREEN + "   [✅] Clicked on confirm button." + RESET)
    
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//mat-dialog-container")))
    print(GREEN + f"[✅] Package '{PACKAGE_NAME}' was deleted successfully!" + RESET)

def test_automation():
    try:
        print_separator()
        print(CYAN + "[🚀] Starting automation test..." + RESET)

        login()
        add_package()
        logout()

        verify_package_exists()
        delete_package()
        logout()

        print_separator()
        print(GREEN + "[🎉] Automation test completed successfully!" + RESET)

    except Exception as e:
        print_separator()
        print(RED + f"[❌] An error occurred: {e}" + RESET)
    
    finally:
        driver.quit()
        print(CYAN + "[🚪] WebDriver session closed." + RESET)

# Execute the function
test_automation()