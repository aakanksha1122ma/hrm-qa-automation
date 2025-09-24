# OrangeHRM QA Automation Project

This project automates the testing of the OrangeHRM demo website using Selenium WebDriver with Python.

## Features

The automation script performs the following actions:
1. Automates the Login Flow
2. Navigates to the PIM module
3. Adds 4 employees to the system
4. Verifies employees in the Employee List
5. Logs out from the Dashboard

## Prerequisites

- Python 3.11 installed
- One or more of the following browsers installed:
  - Chrome
  - Firefox
  - Edge

## Installation

1. Install the required dependencies:
   ```
   py -m pip install -r requirements.txt
   ```

## Usage

Run the automation script:
```
py orangehrm_automation.py
```

To specify a browser, modify the main execution part of the script:
```python
# Change this line to use different browsers
automation = OrangeHRMAutomation("chrome")  # or "firefox" or "edge"
```

## Project Structure

- `orangehrm_automation.py`: Main automation script with support for multiple browsers
- `requirements.txt`: Python dependencies
- `README.md`: This documentation file
- `simple_test.py`: A simplified version for testing basic functionality
- `multi_browser_test.py`: A script that runs tests on multiple browsers sequentially

## How It Works

The script uses Selenium WebDriver to automate browser actions:
- `webdriver-manager` automatically downloads and manages drivers for different browsers
- WebDriverWait and expected_conditions are used to wait for elements to load
- ActionChains is used for mouse hover actions
- The script adds 4 employees with predefined names and IDs
- It then verifies each employee by searching for them in the Employee List

## Expected Output

When running the script, you should see the following printed in the console:
- "Setting up [browser] driver..."
- "[browser] driver setup complete"
- "Login successful"
- "Navigated to PIM module"
- "Employee [First Name] [Last Name] added successfully" (for each employee)
- "Name Verified: [Full Name]" (for each employee)
- "Logout successful"

The script will automatically open the specified browser window and perform all the actions. The browser window will close automatically at the end of the test.

## Troubleshooting

If you encounter issues running the scripts, particularly the "OSError: [WinError 193] %1 is not a valid Win32 application" error, please refer to the TROUBLESHOOTING.md file for detailed solutions.
