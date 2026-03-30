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
    id       = "TC_PL_001"
    name     = "test_addPolicy_manual"
    module   = "Policy Management"
    priority = "High"
    severity = "Critical"
    expected = "Policy created manually; 'Created Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        page.locator(".tiptap").fill("This is a test policy created using Playwright automation.")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Created Successfully")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Policy created successfully", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_addPolicy_Ai(page, login):
    id       = "TC_PL_002"
    name     = "test_addPolicy_Ai"
    module   = "Policy Management"
    priority = "High"
    severity = "Major"
    expected = "AI generates policy; 'Policy generated successfully' then 'Created Successfully' toasts are visible"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        page.get_by_role("button", name="Generate Policy with AI").click()
        page.get_by_role("textbox", name="Enter AI Prompt (e.g. Create").fill("Create a comprehensive policy for data security.")
        page.get_by_role("button", name="Generate Policy", exact=True).click()
        page.wait_for_timeout(5000)
        expect(page.get_by_text("Policy generated successfully")).to_be_visible()
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Created Successfully")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "AI policy created successfully", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_addPolicy_url(page, login):
    id       = "TC_PL_003"
    name     = "test_addPolicy_url"
    module   = "Policy Management"
    priority = "Medium"
    severity = "Major"
    expected = "Policy created from URL; 'Created Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="URL Provide a URL").click()
        page.get_by_role("textbox", name="Enter URL (e.g. https://www.").fill("https://www.cyberensic.ai/")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Created Successfully")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Policy created from URL successfully", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_submit_without_filling(page, login):
    id       = "TC_PL_004"
    name     = "test_submit_without_filling"
    module   = "Policy Management"
    priority = "High"
    severity = "Critical"
    expected = "Validation messages shown for all 6 required fields"

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
        record_result(id, name, module, priority, severity, expected, "All 6 validation messages shown", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_delete_policy(page, login):
    id       = "TC_PL_005"
    name     = "test_delete_policy"
    module   = "Policy Management"
    priority = "High"
    severity = "Critical"
    expected = "'Deleted Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.locator(".inline-flex.cursor-pointer.items-center.justify-center.gap-2.whitespace-nowrap.rounded-sm.text-sm.font-medium.transition-all.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\:not\\(\\[class\\*\\=\\'size-\\'\\]\\)\\]\\:size-4.shrink-0.\\[\\&_svg\\]\\:shrink-0.outline-none.focus-visible\\:border-ring.focus-visible\\:ring-\\[3px\\].aria-invalid\\:ring-destructive\\/20.dark\\:aria-invalid\\:ring-destructive\\/40.aria-invalid\\:border-destructive.bg-destructive").first.click()
        page.get_by_role("button", name="Delete").click()
        expect(page.get_by_text("Deleted Successfully")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Policy deleted successfully", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_update_policy(page, login):
    id       = "TC_PL_006"
    name     = "test_update_policy"
    module   = "Policy Management"
    priority = "High"
    severity = "Major"
    expected = "'Updated Successfully' toast is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.locator("span:nth-child(2) > .inline-flex").first.click()
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").click()
        page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill(f"Test Policy {uuid.uuid4().hex[:8]}")
        page.get_by_role("checkbox", name="File Attach a file").click()
        page.get_by_role("button", name="Update").click()
        expect(page.get_by_text("Updated Successfully")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Policy updated successfully", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_view_policy(page, login):
    id       = "TC_PL_007"
    name     = "test_view_policy"
    module   = "Policy Management"
    priority = "Medium"
    severity = "Minor"
    expected = "'Policy Details' heading is visible"

    try:
        page.goto(f"{APP_URL}/policy")
        page.wait_for_timeout(2000)
        page.locator(".flex.items-center > span > .inline-flex").first.click()
        expect(page.get_by_role("heading", name="Policy Details")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Policy Details page opened", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


# ---------------------------------------------------------------------------
# Negative test cases
# ---------------------------------------------------------------------------

def test_addPolicy_invalid_url(page, login):
    id       = "TC_PL_008"
    name     = "test_addPolicy_invalid_url"
    module   = "Policy Management"
    priority = "Medium"
    severity = "Major"
    expected = "Validation error shown for invalid URL format"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="URL Provide a URL").click()
        page.get_by_role("textbox", name="Enter URL (e.g. https://www.").fill("not-a-valid-url")
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Invalid URL")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Invalid URL error shown", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_addPolicy_empty_manual_content(page, login):
    id       = "TC_PL_009"
    name     = "test_addPolicy_empty_manual_content"
    module   = "Policy Management"
    priority = "High"
    severity = "Major"
    expected = "Validation error shown when manual content is empty"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        # Leave the content editor empty and submit
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Policy content is required")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Content required error shown", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise


def test_addPolicy_empty_ai_prompt(page, login):
    id       = "TC_PL_010"
    name     = "test_addPolicy_empty_ai_prompt"
    module   = "Policy Management"
    priority = "Medium"
    severity = "Minor"
    expected = "Validation error shown when AI prompt is empty"

    try:
        page.goto(f"{APP_URL}/policy")
        add_policy(page)
        page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
        page.get_by_role("button", name="Generate Policy with AI").click()
        # Leave prompt empty and click Generate
        page.get_by_role("textbox", name="Enter AI Prompt (e.g. Create").fill("")
        page.get_by_role("button", name="Generate Policy", exact=True).click()
        page.wait_for_timeout(2000)
        expect(page.get_by_text("Prompt is required")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Prompt required error shown", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise
