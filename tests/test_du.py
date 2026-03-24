import pytest
from playwright.sync_api import expect
import uuid

def test_delete_policy(page,login):
    page.goto("https://dashboard.dev01.cyberensic.ai/policy")
    page.wait_for_timeout(2000)
    # Select all delete buttons using the XPath and click the first one
    page.locator(".inline-flex.cursor-pointer.items-center.justify-center.gap-2.whitespace-nowrap.rounded-sm.text-sm.font-medium.transition-all.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\:not\\(\\[class\\*\\=\\'size-\\'\\]\\)\\]\\:size-4.shrink-0.\\[\\&_svg\\]\\:shrink-0.outline-none.focus-visible\\:border-ring.focus-visible\\:ring-\\[3px\\].aria-invalid\\:ring-destructive\\/20.dark\\:aria-invalid\\:ring-destructive\\/40.aria-invalid\\:border-destructive.bg-destructive").first.click()
    page.get_by_role("button", name="Delete").click()
    expect(page.get_by_text("Deleted Successfully")).to_be_visible()
    
def test_update_policy(page,login):
    page.goto("https://dashboard.dev01.cyberensic.ai/policy")
    page.wait_for_timeout(2000)  
    page.locator("span:nth-child(2) > .inline-flex").first.click()
    page.get_by_role("textbox", name="Enter Name (e.g. Cyber").click() 
    page.get_by_role("textbox", name="Enter Name (e.g. Cyber").fill(f"Test Policy {uuid.uuid4().hex[:8]}")
    page.get_by_role("checkbox", name="File Attach a file").click()
    page.get_by_role("button", name="Update").click()
    expect(page.get_by_text("Updated Successfully")).to_be_visible()
    
def test_view_policy(page,login):
    page.goto("https://dashboard.dev01.cyberensic.ai/policy")
    page.wait_for_timeout(2000)
    page.locator(".flex.items-center > span > .inline-flex").first.click()
    expect(page.get_by_role("heading", name="Policy Details")).to_be_visible()
    
def test_filter_columns_appear(page,login):
    pass

    
    

   
