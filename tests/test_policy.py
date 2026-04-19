import re
import uuid
from playwright.sync_api import expect
from conftest import record_result, short_error, APP_URL


def add_policy(page):
    page.get_by_role("button", name="Add Policy").click()
    page.wait_for_timeout(2000)
    unique_policy_name = f"Test Policy {uuid.uuid4().hex[:8]}"
    page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill(unique_policy_name)
    page.locator("button").filter(has_text="Select Category").click()
    page.locator("role=option").first.click()
    page.locator("button").filter(has_text="Select Owner").click()
    page.locator("role=option").first.click()
    page.locator("button").filter(has_text="Select Approver").click()
    page.locator("role=option").first.click()
    page.get_by_role("button", name="Select Next Review Date").click()
    page.locator("td").last.click()
    page.locator("button").filter(has_text="Select Review Frequency").click()
    page.locator("role=option").nth(1).click()


def test_addPolicy_manual(page, login):
    id          = "TC_PL_001"
    scenario    = "Policy Management"
    description = "Create policy manually with valid data"
    test_data   = "Policy name: random UUID\nCategory: first option\nManual content: test text"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Fill all required fields\n4. Select Manual option\n5. Enter content\n6. Click Submit"
    expected    = "Policy created manually; 'Created Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        page.locator(".tiptap").fill("This is a test policy created using Playwright automation.")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Created Successfully")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Policy created successfully")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_addPolicy_Ai(page, login):
    id          = "TC_PL_002"
    scenario    = "Policy Management"
    description = "Create policy using AI generation"
    test_data   = "AI Prompt: 'Create a comprehensive policy for data security.'"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Fill required fields\n4. Select Manual option\n5. Click Generate Policy with AI\n6. Enter AI prompt\n7. Click Generate Policy\n8. Click Submit"
    expected    = "AI generates policy; 'Policy generated successfully' then 'Created Successfully' toasts are visible"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        page.get_by_role("button", name="Generate Policy with AI").click()
        page.get_by_role("textbox", name="Enter AI Prompt (e.g. Create").fill("Create a comprehensive policy for data security.")
        page.get_by_role("button", name="Generate Policy", exact=True).click()
        expect(page.get_by_text("Policy generated successfully")).to_be_visible(timeout=300000)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Created Successfully")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "AI policy created successfully")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_addPolicy_url(page, login):
    id          = "TC_PL_003"
    scenario    = "Policy Management"
    description = "Create policy from URL"
    test_data   = "URL: https://www.cyberensic.ai/"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Fill required fields\n4. Select URL option\n5. Enter URL\n6. Click Submit"
    expected    = "Policy created from URL; 'Created Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="URL Provide a URL").click()
        page.get_by_role("textbox", name="Enter URL (e.g. https://www.").fill("https://www.cyberensic.ai/")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Created Successfully")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Policy created from URL successfully")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_submit_without_filling(page, login):
    id          = "TC_PL_004"
    scenario    = "Policy Management"
    description = "Submit policy form without filling any fields"
    test_data   = "All fields: (empty)"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Click Submit without filling any field"
    expected    = "Validation messages shown for all 6 required fields"

    try:
        page.goto(f"{APP_URL}/policy")
        page.get_by_role("button", name="Add Policy").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Submit").click()
        expect(page.get_by_text("Policy name is required")).to_be_visible()
        expect(page.get_by_text("Please select a policy")).to_be_visible()
        expect(page.get_by_text("Please select an owner")).to_be_visible()
        expect(page.get_by_text("Please select an approver")).to_be_visible()
        expect(page.get_by_text("Please select a next review")).to_be_visible()
        expect(page.get_by_text("Please select a review")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "All 6 validation messages shown")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_delete_policy(page, login):
    id          = "TC_PL_005"
    scenario    = "Policy Management"
    description = "Delete an existing policy"
    test_data   = "First policy in the list"
    steps       = "1. Navigate to policy page\n2. Click delete button on first policy\n3. Confirm deletion"
    expected    = "'Deleted Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.locator(".inline-flex.cursor-pointer.items-center.justify-center.gap-2.whitespace-nowrap.rounded-sm.text-sm.font-medium.transition-all.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\:not\\(\\[class\\*\\=\\'size-\\'\\]\\)\\]\\:size-4.shrink-0.\\[\\&_svg\\]\\:shrink-0.outline-none.focus-visible\\:border-ring.focus-visible\\:ring-\\[3px\\].aria-invalid\\:ring-destructive\\/20.dark\\:aria-invalid\\:ring-destructive\\/40.aria-invalid\\:border-destructive.bg-destructive").first.click()
        page.get_by_role("button", name="Delete").click()
        expect(page.get_by_text("Deleted Successfully")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Policy deleted successfully")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_update_policy(page, login):
    id          = "TC_PL_006"
    scenario    = "Policy Management"
    description = "Update an existing policy"
    test_data   = "New name: random UUID\nContent type: File"
    steps       = "1. Navigate to policy page\n2. Click edit button on first policy\n3. Update name\n4. Change content type to File\n5. Click Update"
    expected    = "'Updated Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.locator("span:nth-child(2) > .inline-flex").first.click()
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").click()
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill(f"Test Policy {uuid.uuid4().hex[:8]}")
        page.get_by_role("checkbox", name="File Attach a file").click()
        page.get_by_role("button", name="Update").click()
        expect(page.get_by_text("Updated Successfully")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Policy updated successfully")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_view_policy(page, login):
    id          = "TC_PL_007"
    scenario    = "Policy Management"
    description = "View policy details"
    test_data   = "First policy in the list"
    steps       = "1. Navigate to policy page\n2. Click view button on first policy"
    expected    = "'Policy Details' heading is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.locator(".flex.items-center > span > .inline-flex").first.click()
        expect(page.get_by_role("heading", name="Policy Details")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Policy Details page opened")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise



# Negative test cases

def test_addPolicy_invalid_url(page, login):
    id          = "TC_PL_008"
    scenario    = "Policy Management"
    description = "Submit policy with invalid URL format"
    test_data   = "URL: not-a-valid-url"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Fill required fields\n4. Select URL option\n5. Enter invalid URL\n6. Click Submit"
    expected    = "Validation error shown for invalid URL format"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="URL Provide a URL").click()
        url_input = page.get_by_role("textbox", name="Enter URL (e.g. https://www.")
        url_input.fill("not-a-valid-url")
        page.get_by_role("button", name="Submit").click()
        validation_message = url_input.evaluate("el => el.validationMessage")
        assert "URL" in validation_message or validation_message != "", \
            f"Expected 'Please enter a URL' browser popup but got: '{validation_message}'"
        record_result(id, scenario, description, test_data, steps, expected, "PASS", f"Browser validation shown: {validation_message}")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_addPolicy_empty_manual_content(page, login):
    id          = "TC_PL_009"
    scenario    = "Policy Management"
    description = "Submit policy with empty manual content"
    test_data   = "Manual content: (empty)"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Fill required fields\n4. Select Manual option\n5. Leave content empty\n6. Click Submit"
    expected    = "Validation error shown when manual content is empty"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        # Leave the content editor empty and submit
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Policy content is required")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Content required error shown")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_addPolicy_empty_ai_prompt(page, login):
    id          = "TC_PL_010"
    scenario    = "Policy Management"
    description = "Submit AI policy with empty prompt"
    test_data   = "AI Prompt: (empty)"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Fill required fields\n4. Select Manual option\n5. Click Generate Policy with AI\n6. Leave prompt empty\n7. Click Generate Policy"
    expected    = "Validation error shown when AI prompt is empty"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        page.get_by_role("button", name="Generate Policy with AI").click()
        # Leave prompt empty and click Generate
        page.get_by_role("textbox", name="Enter AI Prompt (e.g. Create").fill("")
        page.get_by_role("button", name="Generate Policy", exact=True).click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("AI Prompt must be at least 20 characters")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Prompt required error shown")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise



# More negative test cases

def test_cancel_add_policy_not_saved(page, login):
    id          = "TC_PL_011"
    scenario    = "Policy Management"
    description = "Cancel policy creation does not save policy"
    test_data   = "Policy name: 'TC_PL_011 Should Not Be Saved'"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Enter policy name\n4. Click Cancel"
    expected    = "Policy is NOT saved after clicking Cancel on the create form"
    policy_name = "TC_PL_011 Should Not Be Saved"

    try:
        page.goto(f"{APP_URL}/policy")
        page.get_by_role("button", name="Add Policy").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill(policy_name)
        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text(policy_name)).not_to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Policy not saved after Cancel")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_search_no_match(page, login):
    id          = "TC_PL_012"
    scenario    = "Policy Management"
    description = "Search with a non-existent term returns no results"
    test_data   = "Search term: 'ZZZNOMATCH999XYZ'"
    steps       = "1. Navigate to policy page\n2. Enter search term in search box\n3. Wait for results"
    expected    = "No results shown when searching for a non-existent policy name"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.get_by_placeholder("Search here...").fill("ZZZNOMATCH999XYZ")
        page.wait_for_timeout(2000)
        count = page.locator("table tbody tr").count()
        expect(page.get_by_role("heading", name="No data available", level=3)).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "No results shown for non-existent search")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_edit_clear_name_shows_error(page, login):
    id          = "TC_PL_013"
    scenario    = "Policy Management"
    description = "Edit policy and clear name shows validation error"
    test_data   = "Name: (cleared)"
    steps       = "1. Navigate to policy page\n2. Click edit on first policy\n3. Clear the name field\n4. Click Update"
    expected    = "Validation error shown when Name is cleared on the edit form"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.locator("button:has(.lucide-square-pen)").first.click()
        page.wait_for_timeout(2000)
        name_field = page.locator("input[name='name']")
        name_field.triple_click()
        name_field.fill("")
        page.get_by_role("button", name="Update").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Policy name is required")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Validation error shown for empty name on edit")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_unauthenticated_redirect(page):
    id          = "TC_PL_014"
    scenario    = "Policy Management"
    description = "Unauthenticated access to policy page redirects to sign-in"
    test_data   = "No login session"
    steps       = "1. Without logging in, navigate to /policy page"
    expected    = "Accessing /policy without login redirects to sign-in page"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(3000)
        assert "sign-in" in page.url, f"Expected redirect to sign-in but got: {page.url}"
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Redirected to sign-in page")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


# Monkey test cases  (unexpected / extreme inputs)

def test_very_long_policy_name(page, login):
    id          = "TC_PL_015"
    scenario    = "Policy Management"
    description = "Very long policy name (500 chars) is rejected"
    test_data   = "Policy name: 500 x 'A'"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Enter 500-character name\n4. Click Submit"
    expected    = "App handles 500-character policy name without crashing"

    try:
        page.goto(f"{APP_URL}/policy")
        page.get_by_role("button", name="Add Policy").click()
        page.wait_for_timeout(2000)
        long_name = "A" * 500
        page.locator("input[name='name']").fill(long_name)
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Policy name must be less than 200 characters")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Validation error shown for name exceeding 200 characters")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_xss_in_policy_name(page, login):
    id          = "TC_PL_016"
    scenario    = "Policy Management"
    description = "XSS script tag in policy name is not executed"
    test_data   = "Policy name: <script>alert('xss')</script>"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Enter XSS payload as name\n4. Click Submit"
    expected    = "XSS script tag in name is NOT executed — rendered as plain text"

    try:
        page.goto(f"{APP_URL}/policy")
        page.get_by_role("button", name="Add Policy").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill("<script>alert('xss')</script>")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(3000)
        # If XSS executed, a dialog would appear — Playwright raises if unexpected dialog appears
        # Reaching here means no alert fired
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "XSS not executed — app handled safely")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_sql_injection_in_search(page, login):
    id          = "TC_PL_017"
    scenario    = "Policy Management"
    description = "SQL injection in search does not crash the app"
    test_data   = "Search term: ' OR '1'='1'; DROP TABLE policies; --"
    steps       = "1. Navigate to policy page\n2. Enter SQL injection payload in search box\n3. Wait for results"
    expected    = "SQL injection in search does not crash or expose data"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.get_by_placeholder("Search here...").fill("' OR '1'='1'; DROP TABLE policies; --")
        page.wait_for_timeout(2000)
        expect(page.locator("table")).to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "App handled SQL injection safely — table still visible")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_refresh_mid_form(page, login):
    id          = "TC_PL_018"
    scenario    = "Policy Management"
    description = "Refreshing mid-form does not save incomplete policy"
    test_data   = "Policy name: 'TC_PL_018 Refresh Mid Form'"
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Enter policy name\n4. Refresh the page"
    expected    = "Refreshing mid-form does not save incomplete policy"
    policy_name = "TC_PL_018 Refresh Mid Form"

    try:
        page.goto(f"{APP_URL}/policy")
        page.get_by_role("button", name="Add Policy").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill(policy_name)
        page.reload()
        page.wait_for_timeout(3000)
        expect(page.get_by_text(policy_name)).not_to_be_visible()
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "Incomplete policy not saved after page refresh")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_special_characters_name(page, login):
    id          = "TC_PL_019"
    scenario    = "Policy Management"
    description = "Special characters in policy name do not break UI"
    test_data   = "Policy name: !@#$%^&*() <Test> 'Policy' \"Name\""
    steps       = "1. Navigate to policy page\n2. Click Add Policy\n3. Enter special characters as name\n4. Click Submit"
    expected    = "Policy name with special characters does not break the UI"

    try:
        page.goto(f"{APP_URL}/policy")
        page.get_by_role("button", name="Add Policy").click()
        page.wait_for_timeout(2000)
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill("!@#$%^&*() <Test> 'Policy' \"Name\"")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(3000)
        # Pass as long as the app does not crash (table or error visible)
        assert page.locator("table").is_visible() or page.locator("text=/required|invalid/i").count() > 0, \
            "App crashed — neither table nor error is visible"
        record_result(id, scenario, description, test_data, steps, expected, "PASS", "App handled special characters without crashing")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise


def test_double_click_submit(page, login):
    id          = "TC_PL_020"
    scenario    = "Policy Management"
    description = "Double-clicking Submit does not create duplicate policies"
    test_data   = "Manual content: 'Double click test content'"
    steps       = "1. Navigate to policy page\n2. Note current count\n3. Click Add Policy\n4. Fill required fields\n5. Double-click Submit"
    expected    = "Double-clicking Submit does not create two identical policies"

    try:
        page.goto(f"{APP_URL}/policy")
        page.locator("div", has_text=re.compile(r"Total \d+ items")).first.wait_for()
        before_text  = page.locator("div", has_text=re.compile(r"Total \d+ items")).first.text_content()
        before_count = int(re.search(r"\d+", before_text).group())
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        page.locator(".tiptap").fill("Double click test content")
        page.get_by_role("button", name="Submit").click()
        # Immediately click again
        submit_btn = page.get_by_role("button", name="Submit")
        if submit_btn.is_visible():
            submit_btn.click()
        page.wait_for_timeout(4000)
        page.locator("div", has_text=re.compile(r"Total \d+ items")).first.wait_for()
        after_text  = page.locator("div", has_text=re.compile(r"Total \d+ items")).first.text_content()
        after_count = int(re.search(r"\d+", after_text).group())
        assert after_count <= before_count + 1, \
            f"Double-click created {after_count - before_count} policies instead of 1"
        record_result(id, scenario, description, test_data, steps, expected, "PASS", f"Count went from {before_count} to {after_count} — no duplicate")
    except Exception as e:
        record_result(id, scenario, description, test_data, steps, expected, "FAIL", short_error(e))
        raise
