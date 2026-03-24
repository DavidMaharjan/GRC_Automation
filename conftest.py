import os
import csv
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Test metadata: maps test function name -> (ID, expected result)
# ---------------------------------------------------------------------------
TEST_METADATA = {
    # test_addpolicy.py
    "test_addPolicy_manual": {
        "id": "TC_AP_001",
        "expected": "Policy created manually; 'Created Successfully' toast is visible",
    },
    "test_addPolicy_Ai": {
        "id": "TC_AP_002",
        "expected": "AI generates policy; 'Policy generated successfully' then 'Created Successfully' toasts are visible",
    },
    "test_addPolicy_url": {
        "id": "TC_AP_003",
        "expected": "Policy created from URL; 'Created Successfully' toast is visible",
    },
    "test_submit_without_filling": {
        "id": "TC_AP_004",
        "expected": "Validation messages shown for all 6 required fields",
    },
    # test_login.py  (add entries as needed)
    "test_valid_login": {
        "id": "TC_LG_001",
        "expected": "User is redirected to dashboard after valid credentials",
    },
    "test_invalid_login": {
        "id": "TC_LG_002",
        "expected": "Error message shown for invalid credentials",
    },
}

# Collects one row per test after the call phase
_test_results: list[dict] = []


# ---------------------------------------------------------------------------
# Playwright fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def login(page):
    page.goto("https://dashboard.dev01.cyberensic.ai/sign-in")
    page.get_by_role("textbox", name="Enter your email (eg, john@").fill("maharjandavid4@gmail.com")
    page.get_by_role("textbox", name="Enter your password").fill("Cyberensic@512")
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(5000)


# ---------------------------------------------------------------------------
# Reporting hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Only capture the "call" phase (not setup/teardown)
    if rep.when != "call":
        return

    test_name = item.originalname or item.name
    meta = TEST_METADATA.get(
        test_name,
        {"id": "N/A", "expected": "Test completes without errors"},
    )

    if rep.passed:
        status = "PASS"
        actual = "Test passed as expected"
    elif rep.failed:
        status = "FAIL"
        # Extract the last meaningful line from the traceback
        longrepr = str(rep.longrepr) if rep.longrepr else ""
        actual = longrepr.strip().splitlines()[-1] if longrepr.strip() else "Test failed"
    else:
        status = "SKIP"
        actual = "Test was skipped"

    _test_results.append(
        {
            "Test Case Name": test_name,
            "Test Case ID": meta["id"],
            "Expected Result": meta["expected"],
            "Actual Result": actual,
            "Status": status,
            "Duration (s)": round(rep.duration, 2) if hasattr(rep, "duration") else "",
        }
    )


def pytest_sessionfinish(session, exitstatus):
    if not _test_results:
        return

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    headers = ["Test Case Name", "Test Case ID", "Expected Result", "Actual Result", "Status", "Duration (s)"]

    # ---- CSV ---------------------------------------------------------------
    csv_path = os.path.join("reports", f"test_report_{timestamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        writer.writerows(_test_results)
    print(f"\n[Report] CSV  -> {csv_path}")

    # ---- Excel -------------------------------------------------------------
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Test Results"

        # Header styling
        header_fill = PatternFill("solid", fgColor="2E4057")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        thin = Side(style="thin", color="AAAAAA")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col_idx, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border

        # Data rows
        pass_fill = PatternFill("solid", fgColor="D6F5D6")  # light green
        fail_fill = PatternFill("solid", fgColor="FFD6D6")  # light red
        skip_fill = PatternFill("solid", fgColor="FFF3CD")  # light yellow

        for row_idx, result in enumerate(_test_results, start=2):
            status = result.get("Status", "")
            row_fill = pass_fill if status == "PASS" else (fail_fill if status == "FAIL" else skip_fill)
            for col_idx, key in enumerate(headers, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=result.get(key, ""))
                cell.fill = row_fill
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                cell.border = border

        # Column widths
        col_widths = [30, 15, 55, 55, 10, 14]
        for col_idx, width in enumerate(col_widths, start=1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = width

        ws.row_dimensions[1].height = 30

        xlsx_path = os.path.join("reports", f"test_report_{timestamp}.xlsx")
        wb.save(xlsx_path)
        print(f"[Report] Excel -> {xlsx_path}")

    except ImportError:
        print("[Report] openpyxl not installed — skipping Excel report. Run: pip install openpyxl")
