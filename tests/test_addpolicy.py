import re
from playwright.sync_api import expect
import pytest
import uuid

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
    
def test_addPolicy_manual(page,login):
    page.goto("https://dashboard.dev01.cyberensic.ai/policy")
    add_policy(page)
    page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
    page.locator(".tiptap").fill("This is a test policy created using Playwright automation. It includes all the necessary details and formatting to ensure it meets the requirements for a comprehensive policy document.")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    expect(page.get_by_text("Created Successfully")).to_be_visible()
    
def test_addPolicy_Ai(page,login):
    page.goto("https://dashboard.dev01.cyberensic.ai/policy")
    add_policy(page)
    page.get_by_role("checkbox", name="Manual Write a comprehensive").click()
    page.get_by_role("button", name="Generate Policy with AI").click()
    page.get_by_role("textbox", name="Enter AI Prompt (e.g. Create").fill("Create a comprehensive policy for data security that includes guidelines for data handling, access control, and incident response.")
    page.get_by_role("button", name="Generate Policy", exact=True).click()
    page.wait_for_timeout(5000)
    expect(page.get_by_text("Policy generated successfully")).to_be_visible()
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    expect(page.get_by_text("Created Successfully")).to_be_visible()
    
def test_addPolicy_url(page,login):
    page.goto("https://dashboard.dev01.cyberensic.ai/policy")
    add_policy(page)
    page.get_by_role("checkbox", name="URL Provide a URL").click()
    page.get_by_role("textbox", name="Enter URL (e.g. https://www.").fill("https://www.cyberensic.ai/")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    expect(page.get_by_text("Created Successfully")).to_be_visible()
    


    
def test_submit_without_filling(page,login):
    page.goto("https://dashboard.dev01.cyberensic.ai/policy")
    page.get_by_role("button", name="Add Policy").click()
    page.wait_for_timeout(2000) 
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Policy name is required")).to_be_visible()
    expect(page.get_by_text("Please select a policy")).to_be_visible()
    expect(page.get_by_text("Please select an owner")).to_be_visible()
    expect(page.get_by_text("Please select an approver")).to_be_visible()
    expect(page.get_by_text("Please select a next review")).to_be_visible()
    expect(page.get_by_text("Please select a review")).to_be_visible()
    

    
