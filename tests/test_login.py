from playwright.sync_api import expect
from conftest import record_result, short_error, LOGIN_EMAIL, LOGIN_PASSWORD, APP_URL

SIGN_IN_URL = f"{APP_URL}/sign-in"


# ---------------------------------------------------------------------------
# Positive test cases
# ---------------------------------------------------------------------------

def test_valid_login(page):
    id       = "TC_LG_001"
    name     = "test_valid_login"
    module   = "Authentication"
    priority = "High"
    severity = "Critical"
    expected = "User is redirected to dashboard after valid credentials"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill(LOGIN_EMAIL)
        page.get_by_role("textbox", name="Enter your password").fill(LOGIN_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("GRC Operations Centre")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Login successful", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


# ---------------------------------------------------------------------------
# Negative test cases
# ---------------------------------------------------------------------------

def test_invalid_credentials(page):
    id       = "TC_LG_002"
    name     = "test_invalid_credentials"
    module   = "Authentication"
    priority = "High"
    severity = "Critical"
    expected = "Error message shown for wrong email and password"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill("wrong@example.com")
        page.get_by_role("textbox", name="Enter your password").fill("WrongPassword123")
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Invalid credentials")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Error message displayed", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_login_empty_email(page):
    id       = "TC_LG_003"
    name     = "test_login_empty_email"
    module   = "Authentication"
    priority = "High"
    severity = "Major"
    expected = "Validation error shown when email is empty"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill("")
        page.get_by_role("textbox", name="Enter your password").fill(LOGIN_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Email is required")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Email validation error shown", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_login_empty_password(page):
    id       = "TC_LG_004"
    name     = "test_login_empty_password"
    module   = "Authentication"
    priority = "High"
    severity = "Major"
    expected = "Validation error shown when password is empty"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill(LOGIN_EMAIL)
        page.get_by_role("textbox", name="Enter your password").fill("")
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Password is required")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Password validation error shown", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_login_invalid_email_format(page):
    id       = "TC_LG_005"
    name     = "test_login_invalid_email_format"
    module   = "Authentication"
    priority = "Medium"
    severity = "Minor"
    expected = "Validation error shown for invalid email format (e.g. 'notanemail')"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill("notanemail")
        page.get_by_role("textbox", name="Enter your password").fill(LOGIN_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Invalid email")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Invalid email format error shown", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise
