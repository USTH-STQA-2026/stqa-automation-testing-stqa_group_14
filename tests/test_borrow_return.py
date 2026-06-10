"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
    - Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn"
      (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
    - Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")'
      (*Nút mượn*)
    - After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again
      (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
    - Return button: 'flt-semantics[role="button"]:has-text("Trả sách")'
      (*Nút trả*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, wait_for_flutter,
)
from datetime import datetime, timedelta
from playwright.sync_api import expect
import re
import time

# Helper function: borrow a book book_name at the Books tab
# Note that it also works with book codes
def borrow(page, test_config, book_name):
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
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed".
        (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
        → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)

    Suggested steps (*Gợi ý các bước*):
        1. login(page, test_config)
        2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
           (*Tìm sách Có sẵn*)
        3. Click "Mượn sách này" button inside that book card
           (*Click nút "Mượn sách này" trong sách đó*)
        4. Wait for confirmation dialog, re-enable semantics
           (*Đợi dialog xác nhận, bật lại semantics*)
        5. Click "Mượn" button (confirm button in dialog)
           (*Click nút "Mượn" — nút xác nhận trong dialog*)
        6. Assert: "Đang mượn" or "thành công" appears
           (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)
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

    """NOTE: TC-09 is combined with TC-08

    Reason: As the database is volatile (all data is deleted upon closing tab), it is impossible to verify
    if BOOK001 borrowed in TC-08 has a borrow record created in TC-09. Moreover, it is meaningless to execute
    TC-09 alone since what we want to see is the borrow records created after borrowing a book, not the
    seed data.

    TC-09 is still written separately for the sake of completion.
    """

    # 4.2 check if borrow record is created for BOOK001

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

    # sleep 5 seconds to wait for the toast message to go away
    time.sleep(5)

    assert due_date.date() == (borrow_date + timedelta(days=14)).date(), (
        f"Expected due date {(borrow_date + timedelta(days=14)).date()}, got {due_date.date()}"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    Description (*Mô tả*):
        Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
        (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

    Hints (*Gợi ý*):
        - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
        - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
          (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)
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
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    Description (*Mô tả*):
        Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
        (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

    Hints (*Gợi ý*):
        - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
        - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
          (*Tìm nút "Trả sách"*)
        - Click and verify status change or success message
          (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)
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
    """
    TC-04-13: An active member whose borrow count is 3 borrows a book
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
    """
    TC-04-11: A suspended member whose borrow count is less than 3 borrows an available book
    """
    
    # 1. Login with the account of MEM004
    page.goto(test_config["base_url"], wait_until="load", timeout=60000)
    enable_flutter_semantics(page)
    login(page, test_config)
    enable_flutter_semantics(page)

    # screenshots of program state before borrowing
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()

    # 3. Borrow the book BOOK001
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
    """
    TC-04-12: An expired member whose borrow count is less than 3 borrows an available book
    """

    # 1. Login with the account of MEM005
    page.goto(test_config["base_url"], wait_until="load", timeout=60000)
    enable_flutter_semantics(page)
    login(page, test_config)
    enable_flutter_semantics(page)

    # screenshots of program state before borrowing
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').first.click()
    page.locator('flt-semantics[role="tab"][aria-label="Sách"]').first.click()

    # 3. Borrow the book BOOK001
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

