from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.os_manager import OSType
import time
import traceback
import sys

class OrangeHRMAutomation:
    def __init__(self, browser="chrome"):
        # Setup driver based on browser choice
        print(f"Setting up {browser} driver...")
        try:
            if browser.lower() == "chrome":
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service)
            elif browser.lower() == "firefox":
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service)
            elif browser.lower() == "edge":
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service)
            else:
                raise ValueError("Unsupported browser. Please choose 'chrome', 'firefox', or 'edge'.")
            
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            print(f"{browser} driver setup complete")
        except Exception as e:
            print(f"Failed to set up {browser} driver: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
        
    def login(self, username, password):
        """Automate the Login Flow"""
        print("Navigating to login page...")
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        print("Waiting for username field...")
        
        # Wait for username field and enter credentials
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        print("Username field found, entering credentials...")
        username_field.send_keys(username)
        
        # Enter password
        print("Finding password field...")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        
        # Click login button
        print("Finding and clicking login button...")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for dashboard to load
        print("Waiting for dashboard to load...")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        print("Login successful")
        
    def navigate_to_pim(self):
        """Navigate to the PIM module"""
        # Wait for PIM menu item and hover over it
        pim_menu = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='PIM']")))
        ActionChains(self.driver).move_to_element(pim_menu).click(pim_menu).perform()
        
        # Wait for PIM page to load
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='PIM']")))
        print("Navigated to PIM module")
        
    def add_employee(self, first_name, last_name, employee_id=None):
        """Add a single employee"""
        # Click on Add Employee button
        add_employee_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='oxd-icon bi-plus oxd-button-icon']")))
        add_employee_button.click()
        
        # Wait for Add Employee page to load
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Add Employee']")))
        
        # Fill in employee details
        first_name_field = self.driver.find_element(By.NAME, "firstName")
        last_name_field = self.driver.find_element(By.NAME, "lastName")
        
        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        
        if employee_id:
            employee_id_field = self.driver.find_element(By.XPATH, "//label[text()='Employee Id']//following::input[1]")
            employee_id_field.clear()
            employee_id_field.send_keys(employee_id)
        
        # Click save button
        save_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        save_button.click()
        
        # Wait for success message or employee list page
        try:
            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Success']")))
            print(f"Employee {first_name} {last_name} added successfully")
        except:
            # If no success message, wait for page to load
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Personal Details']")))
            print(f"Employee {first_name} {last_name} added successfully")
        
        # Navigate back to PIM module
        self.navigate_to_pim()
        
    def add_employees(self, employees_data):
        """Add multiple employees"""
        for employee in employees_data:
            first_name = employee["first_name"]
            last_name = employee["last_name"]
            employee_id = employee.get("employee_id", None)
            self.add_employee(first_name, last_name, employee_id)
            
    def verify_employees_in_list(self, employees_data):
        """Verify employees in the Employee List"""
        # Navigate to Employee List
        employee_list_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Employee List']")))
        employee_list_link.click()
        
        # Wait for Employee List page to load
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Employee List']")))
        
        # Verify each employee
        for employee in employees_data:
            first_name = employee["first_name"]
            last_name = employee["last_name"]
            full_name = f"{first_name} {last_name}"
            
            # Scroll and search for employee
            self.search_and_verify_employee(full_name)
            
    def search_and_verify_employee(self, employee_name):
        """Search for an employee in the list and verify"""
        # Find the search input field
        search_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Employee Name']//following::input[1]")))
        
        # Clear the field and enter employee name
        search_field.clear()
        search_field.send_keys(employee_name)
        
        # Click search button
        search_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        search_button.click()
        
        # Wait for search results
        time.sleep(2)
        
        # Check if employee is in the list
        try:
            employee_row = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{employee_name}')]")
            if employee_row:
                print(f"Name Verified: {employee_name}")
            else:
                print(f"Employee {employee_name} not found in list")
        except:
            print(f"Employee {employee_name} not found in list")
            
    def logout(self):
        """Log Out from the Dashboard"""
        # Click on user profile dropdown
        user_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='oxd-userdropdown-name']")))
        user_dropdown.click()
        
        # Click logout button
        logout_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
        logout_button.click()
        
        # Wait for login page to load
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        print("Logout successful")
        
    def run_test(self):
        """Run the complete test scenario"""
        try:
            # Login credentials for OrangeHRM demo
            username = "Admin"
            password = "admin123"
            
            # Employee data to add
            employees_data = [
                {"first_name": "John", "last_name": "Doe", "employee_id": "001"},
                {"first_name": "Jane", "last_name": "Smith", "employee_id": "002"},
                {"first_name": "Robert", "last_name": "Johnson", "employee_id": "003"},
                {"first_name": "Emily", "last_name": "Williams", "employee_id": "004"}
            ]
            
            # 1. Automate the Login Flow
            self.login(username, password)
            
            # 2. Navigate to the PIM module
            self.navigate_to_pim()
            
            # 3. Add Employees
            self.add_employees(employees_data)
            
            # 4. Verify Employees in the Employee List
            self.verify_employees_in_list(employees_data)
            
            # 5. Log Out from the Dashboard
            self.logout()
            
        except Exception as e:
            print(f"Test failed with exception: {str(e)}")
        finally:
            # Close the browser
            self.driver.quit()

if __name__ == "__main__":
    # Create an instance of the automation class and run the test
    # You can specify browser: "chrome", "firefox", or "edge"
    automation = OrangeHRMAutomation("chrome")  # Change to "firefox" or "edge" to use different browsers
    automation.run_test()
