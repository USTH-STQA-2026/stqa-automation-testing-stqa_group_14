"""Borrow and return workflow tests for the library system."""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, wait_for_flutter,
)
from datetime import datetime, timedelta
from playwright.sync_api import expect
import re

def login_with_env_account(page, base_url, email_env, password_env):
    """Log in with credentials from dedicated environment variables."""
    email = os.getenv(email_env)
    password = os.getenv(password_env)
    if not email or not password:
        pytest.skip(f"Missing {email_env} or {password_env} in .env")

    page.goto(base_url, wait_until="load", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

def borrow(page, test_config, book_name):
    """Helper function: borrow a book book_name
    Precondition: must be at the Books tab already

    Works with both book name and book code
    """
    # find the string book_name in aria-label
    available_book = page.locator(f'flt-semantics[role="group"][aria-label*="{book_name}"][aria-label*="Có sẵn"]').first

    # wait for element to be present in DOM just to be sure
    available_book.wait_for(state="attached", timeout=10000)

    # click on borrow
    available_book.get_by_role("button", name="Mượn sách này").click()

    # confirm the borrow
    wait_for_flutter(page, text="Xác nhận")
    flutter_click_button(page, text="Mượn")


def test_borrow_book(page, test_config):
    """TC-08/09: Verify borrowing an available book creates the correct record.

    Precondition: Member account from test_config can log in and BOOK001 is available.
    Input/Action: Borrow BOOK001 and confirm the borrow dialog.
    Expected: BOOK001 becomes borrowed, a borrow record is created, and due date is borrow date + 14 days.
    """

    # 1. Login with the account of MEM002
    page.goto(test_config["base_url"], wait_until="load", timeout=60000)
    enable_flutter_semantics(page)
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Borrow the book BOOK001

    # screenshots of program state before borrowing
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()

    book_name = "BOOK001"
    
    borrow(page, test_config, book_name)

    # 3. Wait for result
    wait_for_flutter(page, text="thành công")
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()

    # 4. Check result (oracle)

    # 4.1 check specifically for BOOK001 if its status has changed to "Borrowed"
    # after borrowing, the text is contained in <span> not aria-label
    # since flt-semantics has only one child <span>, we use has_text instead of has= for simplicity
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()
    borrowed_book = page.locator('flt-semantics').filter(has_text="BOOK001").filter(has_text="Đang mượn").first
    expect(borrowed_book, "BOOK001's status stayed Available: expect changed to Borrowed").to_be_visible()

    # TC-09 evidence is checked here because the new borrow record only exists
    # in the same browser session after BOOK001 is borrowed.

    # navigate to the record tab
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()

    # locate the record for BOOK001
    record = page.locator('flt-semantics[role="group"][aria-label*="Lập trình Flutter cơ bản"][aria-label*="Đang mượn"]').first
    expect(record, "No borrow record created for BOOK001: expect creation").to_be_visible()

    # 4.3 check if due date is correct
    # get aria-label for easier manipulation
    record_aria_label = record.get_attribute("aria-label")

    # search with regex for date in aria-label
    borrow_match = re.search(r'Ngày mượn:\s*(\d{2}/\d{2}/\d{4})', record_aria_label)
    due_match = re.search(r'Hạn trả:\s*(\d{2}/\d{2}/\d{4})', record_aria_label)
    borrow_date = datetime.strptime(borrow_match.group(1), "%d/%m/%Y")
    due_date = datetime.strptime(due_match.group(1), "%d/%m/%Y")

    assert due_date.date() == (borrow_date + timedelta(days=14)).date(), (
        f"Expected due date {(borrow_date + timedelta(days=14)).date()}, got {due_date.date()}"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: Verify the borrow/return tab shows active borrow records.

    Precondition: Member account from test_config can log in.
    Input/Action: Open the Borrow / Return tab.
    Expected: A borrow record with active borrowing status is visible.
    """

    # 1. Login with the account of MEM002
    page.goto(test_config["base_url"], wait_until="load", timeout=60000)
    enable_flutter_semantics(page)
    login(page, test_config)

    # 2. Navigate to the record tab
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()

    # 3. Check for borrowed books
    record = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]').first
    expect(record, "No borrow record BR001: expect BR001").to_be_visible()

def test_return_book(page, test_config):
    """TC-10: Verify returning a borrowed book updates record and book status.

    Precondition: Member account from test_config can log in and has the seeded borrowed book.
    Input/Action: Click the return button for the seeded borrow record.
    Expected: The record becomes returned and the seeded book becomes available again.
    """

    # 1. Login with the account of MEM002
    page.goto(test_config["base_url"], wait_until="load", timeout=60000)
    enable_flutter_semantics(page)
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Switch to record tab
    # screenshots of program state before returning
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()

    # 3. Return BR001 (Kiểm thử phần mềm nhập môn)

    # seed data
    BOOK_NAME = "Kiểm thử phần mềm nhập môn"

    flutter_click_button(page, text="Trả sách")
    wait_for_flutter(page, text="thành công")
    
    # check if borrow record status has changed to "Đã trả"
    borrowed_book = page.locator('flt-semantics').filter(has_text=BOOK_NAME).filter(has_text="Đã trả").first
    expect(borrowed_book, "Borrow record stayed at Borrowing: expect change to Returned").to_be_visible()

    # 4. Go back to see book status changed
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()
    book_stat = page.locator(f'flt-semantics[role="group"][aria-label*="{BOOK_NAME}"][aria-label*="Có sẵn"]')
    expect(book_stat, "BOOK003's status stayed at Borrowed: expect change to Available").to_be_visible()

########################################################
#              Additional test cases                   #
########################################################

def test_borrow_exceed(page, test_config):
    """TC-04-13: Verify the system blocks borrowing beyond the allowed limit.

    Precondition: Member account from test_config can log in.
    Input/Action: Borrow BOOK001, BOOK002, and then BOOK005 in the same session.
    Expected: The final request is denied, BOOK005 stays available, and no BOOK005 record is created.
    """
    # 1. Login with the account of MEM002
    page.goto(test_config["base_url"], wait_until="load", timeout=60000)
    enable_flutter_semantics(page)
    login(page, test_config)
    enable_flutter_semantics(page)

    # screenshots of program state before borrowing
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()

    # 2. Borrow BOOK001, BOOK002, BOOK005
    book_list = ["BOOK001", "BOOK002", "BOOK005"]
    for i in range(3):
        borrow(page, test_config, book_list[i])

    # 3. Check result (oracle)
    # 3.1 Expect refusal
    refusal = page.locator('flt-semantics').filter(has_text="Không thể").first
    expect(refusal, "System accepted the borrow request on the 4th book: expect denial").to_be_visible()

    # 3.2 Expect BOOK005 is still available
    borrowed_book = page.locator('flt-semantics[role="group"][aria-label*="BOOK005"][aria-label*="Có sẵn"]').first
    expect(borrowed_book, "BOOK005's status changed to Borrowed: expect unchanged").to_be_visible()

    # 3.3 Expect no borrow record for BOOK005
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    record = page.locator('flt-semantics[role="group"][aria-label*="Trí tuệ nhân tạo đại cương"][aria-label*="Đang mượn"]').first
    expect(record, "Borrow record was created for BOOK005: expect no creation").not_to_be_visible()

def test_suspended_borrow(page, test_config):
    """TC-04-11: Verify a suspended member cannot borrow an available book.

    Precondition: SUSPENDED_EMAIL and SUSPENDED_PASSWORD are set in the environment.
    Input/Action: Log in with the suspended account and attempt to borrow BOOK001.
    Expected: Suspension error appears, BOOK001 stays available, and no BOOK001 record is created.
    """
    
    # 1. Login with the account of MEM004
    login_with_env_account(
        page,
        test_config["base_url"],
        "SUSPENDED_EMAIL",
        "SUSPENDED_PASSWORD",
    )

    # screenshots of program state before borrowing
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()

    # 2. Borrow the book BOOK001
    book_name = "BOOK001"
    borrow(page, test_config, book_name)


    # 3. Check result (oracle)

    # 3.1 Error message must mention the member being suspended
    # announcement is in <span>
    error_sus = page.locator('flt-semantics').filter(has_text="tạm ngưng").first
    expect(error_sus, "Wrong error message: expect to announce member having been suspended").to_be_visible()

    # 3.2 Book is still available
    borrowed_book = page.locator('flt-semantics[role="group"][aria-label*="BOOK001"][aria-label*="Có sẵn"]').first
    expect(borrowed_book, "BOOK001's status changed to Borrowed: expect change to Available").to_be_visible()

    # 3.3 No borrow record is created for the book
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    record = page.locator('flt-semantics[role="group"][aria-label*="Lập trình Flutter cơ bản"][aria-label*="Đang mượn"]').first
    expect(record, "Borrow record created for BOOK001: expect no creation").not_to_be_visible()

def test_expired_borrow(page, test_config):
    """TC-04-12: Verify an expired member cannot borrow an available book.

    Precondition: EXPIRED_EMAIL and EXPIRED_PASSWORD are set in the environment.
    Input/Action: Log in with the expired account and attempt to borrow BOOK001.
    Expected: Expiration error appears, BOOK001 stays available, and no BOOK001 record is created.
    """

    # 1. Login with the account of MEM005
    login_with_env_account(
        page,
        test_config["base_url"],
        "EXPIRED_EMAIL",
        "EXPIRED_PASSWORD",
    )

    # screenshots of program state before borrowing
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()

    # 2. Borrow the book BOOK001
    book_name = "BOOK001"
    borrow(page, test_config, book_name)


    # 3. Check result (oracle)

    # 3.1 Error message must mention the member being expired
    # announcement is in <span>
    error_exp = page.locator('flt-semantics').filter(has_text="hết hạn").first
    expect(error_exp, "Wrong error message: expect to announce member having expired").to_be_visible()

    # 3.2 Book is still available
    borrowed_book = page.locator('flt-semantics[role="group"][aria-label*="BOOK001"][aria-label*="Có sẵn"]').first
    expect(borrowed_book, "BOOK001's status changed to Borrowed: expect change to Available").to_be_visible()

    # 3.3 No borrow record is created for the book
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    record = page.locator('flt-semantics[role="group"][aria-label*="Lập trình Flutter cơ bản"][aria-label*="Đang mượn"]').first
    expect(record, "Borrow record created for BOOK001: expect no creation").not_to_be_visible()

