# orangehrm_automation.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class OrangeHRMAutomation:
    def __init__(self, browser="chrome"):
        self.browser = browser.lower()

        if self.browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--remote-allow-origins=*")

            # Automatically downloads and uses correct ChromeDriver
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

        elif self.browser == "edge":
            options = EdgeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

            # Automatically downloads and uses correct EdgeDriver
            service = EdgeService(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=options)

        else:
            raise ValueError("Supported browsers are: 'chrome' or 'edge'")

    def open_site(self, url: str):
        """Open a given URL"""
        self.driver.get(url)
        print("Opened:", self.driver.title)

    def quit(self):
        """Close browser"""
        self.driver.quit()


if __name__ == "__main__":
    # Change browser="edge" if you want Edge instead
    automation = OrangeHRMAutomation(browser="chrome")
    automation.open_site("https://opensource-demo.orangehrmlive.com/")
    automation.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class OrangeHRMAutomation:
    def __init__(self):
        # Chrome setup for macOS (M1/M2 compatible)
        options = Options()
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, username, password):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys(username)
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        print("Login successful")

    def navigate_to_pim(self):
        pim_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']")))
        pim_menu.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='PIM']")))
        print("Navigated to PIM module")

    def add_employee(self, first_name, last_name, employee_id=None):
        add_employee_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='oxd-icon bi-plus oxd-button-icon']"))
        )
        add_employee_button.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Add Employee']")))

        first_name_field = self.driver.find_element(By.NAME, "firstName")
        last_name_field = self.driver.find_element(By.NAME, "lastName")
        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)

        if employee_id:
            employee_id_field = self.driver.find_element(By.XPATH, "//label[text()='Employee Id']//following::input[1]")
            employee_id_field.clear()
            employee_id_field.send_keys(employee_id)

        save_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        save_button.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Personal Details']")))
        print(f"Employee {first_name} {last_name} added successfully")
        time.sleep(1)
        self.navigate_to_pim()

    def add_employees(self, employees_data):
        for employee in employees_data:
            self.add_employee(employee["first_name"], employee["last_name"], employee.get("employee_id"))

    def verify_employees_in_list(self, employees_data):
        employee_list_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Employee List']")))
        employee_list_link.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Employee List']")))

        for employee in employees_data:
            full_name = f"{employee['first_name']} {employee['last_name']}"
            self.search_and_verify_employee(full_name)

    def search_and_verify_employee(self, employee_name):
        search_field = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//label[text()='Employee Name']//following::input[1]"))
        )
        search_field.clear()
        search_field.send_keys(employee_name)
        search_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        search_button.click()
        time.sleep(2)
        try:
            self.driver.find_element(By.XPATH, f"//div[contains(text(), '{employee_name}')]")
            print(f"Name Verified: {employee_name}")
        except:
            print(f"Employee {employee_name} not found in list")

    def logout(self):
        user_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='oxd-userdropdown-name']")))
        user_dropdown.click()
        logout_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
        logout_button.click()
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        print("Logout successful")

    def run_test(self):
        try:
            username = "Admin"
            password = "admin123"
            employees_data = [
                {"first_name": "John", "last_name": "Doe", "employee_id": "001"},
                {"first_name": "Jane", "last_name": "Smith", "employee_id": "002"},
            ]

            self.login(username, password)
            self.navigate_to_pim()
            self.add_employees(employees_data)
            self.verify_employees_in_list(employees_data)
            self.logout()

        except Exception as e:
            print(f"Test failed with exception: {str(e)}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    automation = OrangeHRMAutomation()
    automation.run_test()