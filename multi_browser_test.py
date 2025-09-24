from orangehrm_automation import OrangeHRMAutomation
import time

def run_test_on_browser(browser_name):
    """Run the OrangeHRM test on a specific browser"""
    print(f"\n{'='*50}")
    print(f"Running test on {browser_name.upper()}")
    print(f"{'='*50}")
    
    try:
        # Create an instance of the automation class with the specified browser
        automation = OrangeHRMAutomation(browser_name)
        automation.run_test()
        print(f"Test completed successfully on {browser_name}")
    except Exception as e:
        print(f"Test failed on {browser_name} with exception: {str(e)}")
        return False
    
    return True

def run_tests_on_multiple_browsers():
    """Run tests on multiple browsers"""
    browsers = ["chrome", "firefox", "edge"]
    results = {}
    
    for browser in browsers:
        try:
            # Run test on each browser
            success = run_test_on_browser(browser)
            results[browser] = success
            
            # Add a delay between tests
            time.sleep(2)
        except Exception as e:
            print(f"Could not run test on {browser}: {str(e)}")
            results[browser] = False
    
    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    for browser, success in results.items():
        status = "PASSED" if success else "FAILED"
        print(f"{browser.upper()}: {status}")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    print(f"\nPassed: {passed_tests}/{total_tests} browser tests")

if __name__ == "__main__":
    run_tests_on_multiple_browsers()
