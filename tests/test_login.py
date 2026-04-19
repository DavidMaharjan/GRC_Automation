from playwright.sync_api import expect
from conftest import record_result, short_error, LOGIN_EMAIL, LOGIN_PASSWORD, APP_URL

SIGN_IN_URL = f"{APP_URL}/sign-in"



# Positive test cases


def test_valid_login(page):
    id          = "TC_LG_001"
    scenario    = "Authentication"
    description = "Valid login with correct credentials"
    test_data   = "Email: valid user from .env\nPassword: valid password from .env"
    steps       = "1. Navigate to sign-in page\n2. Enter valid email\n3. Enter valid password\n4. Click Sign In"
    expected    = "User is redirected to dashboard after valid credentials"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill(LOGIN_EMAIL)
        page.get_by_role("textbox", name="Enter your password").fill(LOGIN_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("GRC Operations Centre")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Login successful")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise



# Negative test cases

def test_invalid_credentials(page):
    id          = "TC_LG_002"
    scenario    = "Authentication"
    description = "Login with wrong email and wrong password"
    test_data   = "Email: wrong@example.com\nPassword: WrongPassword123"
    steps       = "1. Navigate to sign-in page\n2. Enter wrong email\n3. Enter wrong password\n4. Click Sign In"
    expected    = "Error message shown for wrong email and password"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill("wrong@example.com")
        page.get_by_role("textbox", name="Enter your password").fill("WrongPassword123")
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Sign-in failed")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Error message displayed")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_valid_email_wrong_password(page):
    id          = "TC_LG_003"
    scenario    = "Authentication"
    description = "Login with valid email but wrong password"
    test_data   = "Email: valid from .env\nPassword: WrongPassword123"
    steps       = "1. Navigate to sign-in page\n2. Enter valid email\n3. Enter wrong password\n4. Click Sign In"
    expected    = "Error message shown when correct email is used with wrong password"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill(LOGIN_EMAIL)
        page.get_by_role("textbox", name="Enter your password").fill("WrongPassword123")
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Password is incorrect. Try again, or use another method.")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Sign-in failed error shown")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_login_empty_email(page):
    id          = "TC_LG_004"
    scenario    = "Authentication"
    description = "Login with empty email field"
    test_data   = "Email: (empty)\nPassword: valid from .env"
    steps       = "1. Navigate to sign-in page\n2. Leave email blank\n3. Enter valid password\n4. Click Sign In"
    expected    = "Validation error shown when email is empty"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill("")
        page.get_by_role("textbox", name="Enter your password").fill(LOGIN_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Email is required")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Email validation error shown")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_login_empty_password(page):
    id          = "TC_LG_005"
    scenario    = "Authentication"
    description = "Login with empty password field"
    test_data   = "Email: valid from .env\nPassword: (empty)"
    steps       = "1. Navigate to sign-in page\n2. Enter valid email\n3. Leave password blank\n4. Click Sign In"
    expected    = "Validation error shown when password is empty"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter your email (eg, john@").fill(LOGIN_EMAIL)
        page.get_by_role("textbox", name="Enter your password").fill("")
        page.get_by_role("button", name="Sign In").click()
        expect(page.get_by_text("Password is required")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Password validation error shown")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_login_invalid_email_format(page):
    id          = "TC_LG_006"
    scenario    = "Authentication"
    description = "Login with invalid email format"
    test_data   = "Email: notanemail\nPassword: valid from .env"
    steps       = "1. Navigate to sign-in page\n2. Enter 'notanemail' as email\n3. Enter valid password\n4. Click Sign In"
    expected    = "Validation error shown for invalid email format (e.g. 'notanemail')"

    try:
        page.goto(SIGN_IN_URL)
        page.wait_for_timeout(2000)
        email_input = page.get_by_role("textbox", name="Enter your email (eg, john@")
        email_input.fill("notanemail")
        page.get_by_role("textbox", name="Enter your password").fill(LOGIN_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        validation_message = email_input.evaluate("el => el.validationMessage")
        assert "@" in validation_message, f"Expected browser validation for invalid email, got: '{validation_message}'"
        record_result(id, scenario, description, test_data, steps, expected, "PASS", f"Browser validation: {validation_message}")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise
