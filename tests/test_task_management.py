import re
import uuid
from playwright.sync_api import expect
from conftest import record_result, short_error, APP_URL

def add_project(page, name=None, description=None):
    page.goto(f"{APP_URL}/manage-projects")
    page.get_by_role("button", name="Add Project").click()
    project_name = name or f"Test Project {uuid.uuid4().hex[:8]}"
    project_desc = description or "This is a test project"
    page.get_by_role("textbox", name="Enter project name (e.g.").fill(project_name)
    page.get_by_role("textbox", name="Enter project description (e.").fill(project_desc)
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Created Successfully")).to_be_visible()
    return project_name

def test_add_project(page, login):
    id = "TC_TM_001"
    name = "test_add_project"
    module = "Task Management"
    priority = "High"
    severity = "Critical"
    expected = "Project created successfully"
    try:
        project_name = add_project(page)
        record_result(id, name, module, priority, severity, expected, f"Project '{project_name}' created", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise

def test_edit_project(page, login):
    id = "TC_TM_002"
    name = "test_edit_project"
    module = "Task Management"
    priority = "High"
    severity = "Major"
    expected = "Project updated successfully"
    try:
        project_name = add_project(page)
        page.locator(".flex > .flex > span:nth-child(2) > .inline-flex").first.click()
        new_name = f"{project_name}-edited"
        page.get_by_role("textbox", name="Enter project name (e.g.").fill(new_name)
        page.get_by_role("textbox", name="Enter project description (e.").fill("This is a test project-edited")
        page.get_by_role("button", name="Update").click()
        expect(page.get_by_text("Updated Successfully")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, f"Project '{new_name}' updated", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise

def test_view_project_details(page, login):
    id = "TC_TM_003"
    name = "test_view_project_details"
    module = "Task Management"
    priority = "Medium"
    severity = "Minor"
    expected = "Project details page is visible"
    try:
        project_name = add_project(page)
        page.locator(".flex > .flex > span > .inline-flex").first.click()
        expect(page.get_by_role("heading", name="Project Details")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Project details viewed", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise

def test_open_task_board(page, login):
    id = "TC_TM_004"
    name = "test_open_task_board"
    module = "Task Management"
    priority = "Medium"
    severity = "Minor"
    expected = "Task board tab is visible"
    try:
        project_name = add_project(page)
        page.locator(".flex > .flex > span > .inline-flex").first.click()
        page.get_by_role("tab", name="Board").click()
        expect(page.get_by_role("tab", name="Board")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, "Task board opened", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise

def test_delete_project(page, login):
    id = "TC_TM_005"
    name = "test_delete_project"
    module = "Task Management"
    priority = "High"
    severity = "Critical"
    expected = "Project deleted successfully"
    try:
        project_name = add_project(page)
        page.locator(".inline-flex.cursor-pointer.items-center.justify-center.gap-2.whitespace-nowrap.rounded-sm.text-sm.font-medium.transition-all.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\:not\\(\\[class\\*\\=\\'size-\\'\\]\\)\\]\\:size-4.shrink-0.\\[\\&_svg\\]\\:shrink-0.outline-none.focus-visible\\:border-ring.focus-visible\\:ring-\\[3px\\].aria-invalid\\:ring-destructive\\/20.dark\\:aria-invalid\\:ring-destructive\\/40.aria-invalid\\:border-destructive.bg-destructive").first.click()
        page.get_by_role("button", name="Delete").click()
        expect(page.get_by_text("Deleted Successfully")).to_be_visible()
        record_result(id, name, module, priority, severity, expected, f"Project '{project_name}' deleted", "PASS")
    except Exception as e:
        record_result(id, name, module, priority, severity, expected, short_error(e), "FAIL")
        raise
    
    