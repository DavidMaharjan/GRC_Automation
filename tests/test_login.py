from playwright.sync_api import expect
import pytest
def report_test_result(test_case_name, test_case_id, expected_result, actual_result, status):
    with open("reports/results.txt", "a") as f:
        f.write(f"Test Case Name: {test_case_name}\n")
        f.write(f"Test Case ID: {test_case_id}\n")
        f.write(f"Expected Result: {expected_result}\n")
        f.write(f"Actual Result: {actual_result}\n")
        f.write(f"Status: {status}\n")
        f.write("-" * 40 + "\n")
        
def test_login(page):
    test_case_name = "test_login"
    test_case_id = "TC001"
    expected_result = "User should be able to login successfully"
    try:
        page.goto("https://dashboard.dev01.cyberensic.ai/sign-in")
        page.wait_for_timeout(2000)
        email = page.get_by_role("textbox", name="Enter your email (eg, john@")
        password = page.get_by_role("textbox", name="Enter your password")
        email.fill("maharjandavid4@gmail.com")
        password.fill("Cyberensic@512")
        page.get_by_role("button", name="Sign In").click()
        page.wait_for_timeout(5000)
    
        expect(page.locator("GRC Operations Centre")).to_be_visible()
        actual_result = "Login successful"
        status = "PASS"
        
    except Exception as e:
        actual_result = f"Login failed: {e}"
        status = "FAIL"
    report_test_result(test_case_name, test_case_id, expected_result, actual_result, status)
    
