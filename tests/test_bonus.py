import os
import re
import pytest
from dotenv import load_dotenv

from conftest import (
    enable_flutter_semantics,
    flutter_click_button,
    flutter_fill,
    wait_for_flutter,
)


load_dotenv()

PASSWORD_LABEL = "Mật khẩu"
LOGIN_BUTTON = "Đăng nhập"
LOGOUT_BUTTON = "Đăng xuất"
BOOKS_TAB = "Sách"
BORROW_TAB = "Mượn / Trả"
MEMBERS_TAB = "Thành viên"
MY_BORROWS_TAB = "Phiếu mượn của tôi"
LOOKUP_TAB = "Tra cứu phiếu mượn"
LOOKUP_LABEL = "Nhập mã thành viên (VD: MEM001)"
ADD_MEMBER_BUTTON = "Thêm thành viên"
FULL_NAME_LABEL = "Họ và tên"
PHONE_LABEL = "Số điện thoại"
RETURN_BUTTON = "Trả sách"
RETURNED_STATUS = "Đã trả"
BORROWING_STATUS = "Đang mượn"
AVAILABLE_STATUS = "Có sẵn"
OVERDUE = "Quá hạn"


def _require_env(*names):
    missing = [name for name in names if not os.getenv(name)]
    if missing:
        pytest.skip(f"Missing required environment variable(s): {', '.join(missing)}")
    return [os.getenv(name) for name in names]


def _mock_date(page, iso_date):
    page.add_init_script(
        f"""
        (() => {{
          const fixed = new Date('{iso_date}T12:00:00');
          const RealDate = Date;
          class MockDate extends RealDate {{
            constructor(...args) {{
              if (args.length === 0) {{
                super(fixed.getTime());
              }} else {{
                super(...args);
              }}
            }}
            static now() {{
              return fixed.getTime();
            }}
          }}
          MockDate.UTC = RealDate.UTC;
          MockDate.parse = RealDate.parse;
          MockDate.prototype = RealDate.prototype;
          window.Date = MockDate;
        }})();
        """
    )


def _login(page, base_url, email, password):
    page.goto(base_url, wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", email)
    flutter_fill(page, PASSWORD_LABEL, password)
    flutter_click_button(page, LOGIN_BUTTON)
    wait_for_flutter(page, text=LOGOUT_BUTTON, timeout=15000)
    enable_flutter_semantics(page)


def _login_member(page, test_config):
    if not test_config["email"] or not test_config["password"]:
        pytest.skip("Missing TEST_EMAIL or TEST_PASSWORD in environment")
    _login(page, test_config["base_url"], test_config["email"], test_config["password"])


def _login_other(page, test_config):
    email, password = _require_env("MEMBER_OTHER_EMAIL", "MEMBER_OTHER_PASSWORD")
    _login(page, test_config["base_url"], email, password)


def _login_librarian(page, test_config):
    email, password = _require_env("LIBRARIAN_EMAIL", "LIBRARIAN_PASSWORD")
    _login(page, test_config["base_url"], email, password)


def _open_tab(page, tab_name):
    tab = page.locator(f'flt-semantics[role="tab"][aria-label="{tab_name}"]').first
    if tab.count() == 0:
        return False
    tab.click()
    enable_flutter_semantics(page)
    return True


def _open_returns(page):
    if not _open_tab(page, BORROW_TAB):
        pytest.skip("Borrow / Return tab is not available")
    page.locator(
        f'flt-semantics[role="tab"][aria-label="{MY_BORROWS_TAB}"], '
        f'flt-semantics[role="tab"][aria-label="{LOOKUP_TAB}"], '
        f'flt-semantics:has-text("{RETURN_BUTTON}")'
    ).first.wait_for(state="attached", timeout=10000)
    enable_flutter_semantics(page)


def _open_members(page):
    if not _open_tab(page, MEMBERS_TAB):
        pytest.skip("Members tab is not available")
    wait_for_flutter(page, text=ADD_MEMBER_BUTTON, timeout=10000)


def _open_add(page):
    _open_members(page)
    flutter_click_button(page, ADD_MEMBER_BUTTON)
    page.locator(f'input[aria-label="{FULL_NAME_LABEL}"]').first.wait_for(
        state="attached",
        timeout=10000,
    )
    enable_flutter_semantics(page)


def _records(page):
    return page.locator(
        'flt-semantics[role="group"]:has-text("Mã phiếu"), '
        'flt-semantics[role="group"][aria-label*="Mã phiếu"]'
    )


def _text(group):
    visible_text = group.text_content(timeout=2000) or ""
    aria_label = group.get_attribute("aria-label", timeout=2000) or ""
    return f"{visible_text}\n{aria_label}"


def _page_text(page):
    enable_flutter_semantics(page)
    text_parts = page.locator("flt-semantics").all_text_contents()
    aria_parts = page.locator("flt-semantics").evaluate_all(
        "(els) => els.map((el) => el.getAttribute('aria-label') || '')"
    )
    return " ".join(text_parts + aria_parts)


def _record(page, code):
    records = _records(page)
    for index in range(records.count()):
        record = records.nth(index)
        record_text = _text(record)
        if code in record_text:
            return record, record_text
    return None, ""


def _owner(record_text):
    match = re.search(r"Thành viên:\s*([^\n]+)", record_text)
    return match.group(1).strip() if match else ""


def _current_user(page):
    candidates = []
    for text in page.locator("flt-semantics").all_text_contents():
        match = re.search(r"([^\n]+?)\s*\(Thành viên\)", text)
        if match:
            candidates.append(match.group(1).strip())
    candidates = [value for value in candidates if "Thư Viện" not in value and len(value) < 80]
    return min(candidates, key=len) if candidates else os.getenv("MEMBER_OTHER_DISPLAY_NAME", "")


def _return_buttons(record):
    return record.locator(f'flt-semantics[role="button"]:has-text("{RETURN_BUTTON}")')


def _click_return(record):
    button = _return_buttons(record)
    if button.count() == 0:
        pytest.fail(f"Return button is missing for record: {_text(record)}")
    button.first.click()


def _submit_member(page, name, email, phone):
    flutter_fill(page, FULL_NAME_LABEL, name)
    flutter_fill(page, "Email", email)
    flutter_fill(page, PHONE_LABEL, phone)
    flutter_click_button(page, ADD_MEMBER_BUTTON)
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)


def _assert_email_error(page, email):
    page_text = _page_text(page)
    assert "thành công" not in page_text.lower(), (
        f"System accepted invalid member email: {email}. Page text: {page_text}"
    )
    assert "email" in page_text.lower() and "hợp lệ" in page_text.lower(), (
        f"System did not display an email validation error for {email}. "
        f"Page text: {page_text}"
    )


def _assert_returned(page, record_code, book_name):
    page_text = _page_text(page)
    assert OVERDUE in page_text or "overdue" in page_text.lower(), (
        "System did not display a clear overdue warning when returning an "
        f"overdue/boundary record. Page text: {page_text}"
    )

    _, record_text = _record(page, record_code)
    assert RETURNED_STATUS in record_text or "Returned" in record_text, (
        f"Borrow record {record_code} did not change to returned. "
        f"Record text: {record_text}"
    )

    assert _open_tab(page, BOOKS_TAB), "Books tab is not available"
    book = page.locator(
        f'flt-semantics[role="group"][aria-label*="{book_name}"]'
        f'[aria-label*="{AVAILABLE_STATUS}"]'
    ).first
    book.wait_for(state="attached", timeout=10000)


def test_due_date(page, test_config):
    """TC-05-02: Return a book on the due date boundary."""
    _mock_date(page, "2024-09-15")
    _login_member(page, test_config)
    _open_returns(page)
    _open_tab(page, MY_BORROWS_TAB)

    record, record_text = _record(page, "BR001")
    assert record is not None, "Expected active borrow record BR001 to exist"
    assert "15/09/2024" in record_text, f"BR001 due date is not visible: {record_text}"

    _click_return(record)
    wait_for_flutter(page, text="thành công", timeout=10000)
    _assert_returned(page, "BR001", "Kiểm thử phần mềm nhập môn")


def test_overdue_book(page, test_config):
    """TC-05-03: Return an overdue borrowed book."""
    _mock_date(page, "2026-05-27")
    _login_member(page, test_config)
    _open_returns(page)
    _open_tab(page, MY_BORROWS_TAB)

    record, record_text = _record(page, "BR001")
    assert record is not None, "Expected active overdue borrow record BR001 to exist"
    assert BORROWING_STATUS in record_text, f"BR001 is not active: {record_text}"

    _click_return(record)
    wait_for_flutter(page, text="thành công", timeout=10000)
    _assert_returned(page, "BR001", "Kiểm thử phần mềm nhập môn")


def test_valid_member(page, test_config):
    """TC-07-01: Add a new member with a valid email."""
    _login_librarian(page, test_config)
    _open_add(page)

    email = "newmember@test.com"
    _submit_member(page, "Nguyen Van Test", email, "0901234567")

    page_text = _page_text(page)
    assert "thành công" in page_text.lower(), (
        f"System did not create a valid member. Page text: {page_text}"
    )

    back = page.locator('flt-semantics[role="button"]:has-text("Quay lại")').first
    if back.count() > 0:
        back.click()
        enable_flutter_semantics(page)

    assert email in _page_text(page), f"New member {email} does not appear in the member list"


def test_domain_dot(page, test_config):
    """TC-07-02: Reject email missing a dot in the domain."""
    _login_librarian(page, test_config)
    _open_add(page)
    _submit_member(page, "Missing Domain Dot", "user@domain", "0901234568")
    _assert_email_error(page, "user@domain")


def test_no_at(page, test_config):
    """TC-07-03: Reject email missing @."""
    _login_librarian(page, test_config)
    _open_add(page)
    _submit_member(page, "Missing At", "userdomain.com", "0901234569")
    _assert_email_error(page, "userdomain.com")


def test_duplicate_email(page, test_config):
    """TC-07-04: Reject duplicate member email."""
    _login_librarian(page, test_config)
    _open_add(page)
    _submit_member(page, "Duplicate Email", "ba.nguyen@email.com", "0901234570")

    page_text = _page_text(page)
    assert "thành công" not in page_text.lower(), (
        f"System accepted a duplicate email. Page text: {page_text}"
    )
    assert "tồn tại" in page_text.lower() or "already" in page_text.lower(), (
        "System did not show an email-already-exists message for duplicate "
        f"email. Page text: {page_text}"
    )


def test_member_tab(page, test_config):
    """TC-07-05: Member account cannot access the Members tab."""
    _login_member(page, test_config)
    members_tab = page.locator(f'flt-semantics[role="tab"][aria-label="{MEMBERS_TAB}"]')
    assert members_tab.count() == 0, "Members tab is visible to a normal member"


def test_foreign_return(page, test_config):
    """TC-05-05: Member cannot return another member's borrowed book."""
    _login_other(page, test_config)
    _open_returns(page)
    if not _open_tab(page, LOOKUP_TAB):
        pytest.skip("Borrow lookup tab is not available")

    flutter_fill(page, LOOKUP_LABEL, "MEM002")
    flutter_click_button(page, "Tra cứu")
    enable_flutter_semantics(page)

    current_user = _current_user(page)
    record, record_text = _record(page, "BR001")
    if record is None:
        assert "BR001" not in _page_text(page), "Foreign record BR001 should not be visible"
        return

    owner = _owner(record_text)
    is_foreign = owner and current_user and owner != current_user
    assert is_foreign, f"BR001 is not a foreign record in this test context: {record_text}"
    assert RETURN_BUTTON not in record_text and _return_buttons(record).count() == 0, (
        "Return Book is available for a borrow record owned by another member. "
        f"Current user: {current_user}; record text: {record_text}"
    )
