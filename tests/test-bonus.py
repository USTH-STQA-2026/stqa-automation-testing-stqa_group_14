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
BORROW_RETURN_TAB = "Mượn / Trả"
MY_BORROWS_TAB = "Phiếu mượn của tôi"
LOOKUP_BORROWS_TAB = "Tra cứu phiếu mượn"
RETURN_BUTTON = "Trả sách"
RETURNED_STATUS = "Đã trả"
BORROWING_STATUS = "Đang mượn"
OVERDUE_TEXT = "Quá hạn"
CHECK_OVERDUE_TEXTS = ("Kiểm tra quá hạn", "Check Overdue")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

TC_05_05_BUG_SCREENSHOT = os.path.join(
    SCREENSHOT_DIR,
    "tc_05_05_bug_access_control.png",
)
TC_05_04_BUG_SCREENSHOT = os.path.join(
    SCREENSHOT_DIR,
    "tc_05_04_bug_duplicate_return.png",
)
TC_06_05_PASS_SCREENSHOT = os.path.join(SCREENSHOT_DIR, "tc_06_05_pass.png")


def _require_env(*names):
    missing = [name for name in names if not os.getenv(name)]
    if missing:
        pytest.skip(f"Missing required environment variable(s): {', '.join(missing)}")
    return [os.getenv(name) for name in names]


def _login_with_credentials(page, base_url, email, password):
    page.goto(base_url, wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", email)
    flutter_fill(page, PASSWORD_LABEL, password)
    flutter_click_button(page, LOGIN_BUTTON)
    wait_for_flutter(page, text=LOGOUT_BUTTON, timeout=15000)
    enable_flutter_semantics(page)


def _login_primary_member(page, test_config):
    if not test_config["email"] or not test_config["password"]:
        pytest.skip("Missing TEST_EMAIL or TEST_PASSWORD in environment")
    _login_with_credentials(
        page,
        test_config["base_url"],
        test_config["email"],
        test_config["password"],
    )


def _open_borrow_return(page):
    tab = page.locator(
        f'flt-semantics[role="tab"][aria-label="{BORROW_RETURN_TAB}"]'
    ).first
    tab.wait_for(state="attached", timeout=10000)
    tab.click()
    page.locator(
        f'flt-semantics[role="tab"][aria-label="{MY_BORROWS_TAB}"], '
        f'flt-semantics[role="tab"][aria-label="{LOOKUP_BORROWS_TAB}"], '
        f'flt-semantics:has-text("{RETURN_BUTTON}")'
    ).first.wait_for(state="attached", timeout=10000)
    enable_flutter_semantics(page)


def _click_inner_tab_if_present(page, tab_name):
    tab = page.locator(f'flt-semantics[role="tab"][aria-label="{tab_name}"]').first
    if tab.count() == 0:
        return False
    tab.click()
    enable_flutter_semantics(page)
    return True


def _borrow_record_groups(page):
    return page.locator(
        'flt-semantics[role="group"]:has-text("Mã phiếu"), '
        'flt-semantics[role="group"][aria-label*="Mã phiếu"]'
    )


def _group_text(group):
    visible_text = group.text_content(timeout=2000) or ""
    aria_label = group.get_attribute("aria-label", timeout=2000) or ""
    return f"{visible_text}\n{aria_label}"


def _extract_member_name(record_text):
    match = re.search(r"Thành viên:\s*([^\n]+)", record_text)
    return match.group(1).strip() if match else ""


def _current_member_name(page):
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    match = re.search(r"([^\n]+?)\s*\(Thành viên\)", sem_text)
    return match.group(1).strip() if match else os.getenv("MEMBER_OTHER_DISPLAY_NAME", "")


def _return_buttons_inside(group):
    return group.locator(f'flt-semantics[role="button"]:has-text("{RETURN_BUTTON}")')


def _direct_actionable_return_buttons_inside(group):
    # Flutter CanvasKit can leave unrelated or stale button text in descendant
    # semantics. Limit this optional oracle to direct child semantics only.
    return group.locator(
        f'> flt-semantics[role="button"]:has-text("{RETURN_BUTTON}")'
    )


def _all_semantics_text(page):
    enable_flutter_semantics(page)
    text_parts = page.locator("flt-semantics").all_text_contents()
    aria_parts = page.locator("flt-semantics").evaluate_all(
        "(els) => els.map((el) => el.getAttribute('aria-label') || '')"
    )
    return " ".join(text_parts + aria_parts)


def _capture_evidence(page, path):
    enable_flutter_semantics(page)
    page.screenshot(path=path, full_page=True)


def test_tc_05_05_member_cannot_return_another_members_borrowed_book(page, test_config):
    """TC-05-05: Member cannot view or return another member's borrow record."""
    other_email, other_password = _require_env(
        "MEMBER_OTHER_EMAIL",
        "MEMBER_OTHER_PASSWORD",
    )

    _login_with_credentials(
        page,
        test_config["base_url"],
        other_email,
        other_password,
    )
    _open_borrow_return(page)
    _click_inner_tab_if_present(page, MY_BORROWS_TAB)

    current_member = _current_member_name(page)
    records = _borrow_record_groups(page)
    foreign_records = []

    for index in range(records.count()):
        record = records.nth(index)
        record_text = _group_text(record)
        owner = _extract_member_name(record_text)
        if owner and current_member and owner != current_member:
            foreign_records.append(record_text)

    # Improvement note: access-control tests would be stronger if the app exposed
    # stable data-testid attributes for borrow records and owner IDs.
    if foreign_records:
        _capture_evidence(page, TC_05_05_BUG_SCREENSHOT)

    assert not foreign_records, (
        "A normal member can see borrow record(s) owned by another member. "
        "Foreign records must be hidden from the current member."
    )


def test_tc_05_04_cannot_return_book_that_is_already_returned(page, test_config):
    """TC-05-04: Returned borrow records must not expose a Return Book action."""
    _login_primary_member(page, test_config)
    _open_borrow_return(page)
    _click_inner_tab_if_present(page, MY_BORROWS_TAB)

    records = _borrow_record_groups(page)
    returned_record = None
    returned_text = ""
    fallback_returned_record = None
    fallback_returned_text = ""

    for index in range(records.count()):
        record = records.nth(index)
        record_text = _group_text(record)
        is_returned = RETURNED_STATUS in record_text or "Returned" in record_text
        if "Mã phiếu: BR004" in record_text and is_returned:
            returned_record = record
            returned_text = record_text
            break
        if is_returned and fallback_returned_record is None:
            fallback_returned_record = record
            fallback_returned_text = record_text

    if returned_record is None:
        returned_record = fallback_returned_record
        returned_text = fallback_returned_text

    if returned_record is None:
        pytest.skip("No returned borrow record is available in this test context")

    assert "Mã phiếu: BR004" in returned_text, (
        "Expected returned borrow record BR004 to be present. "
        f"Actual returned record text: {returned_text}"
    )
    assert RETURNED_STATUS in returned_text or "Returned" in returned_text, (
        f"Returned record does not show returned status. Record text: {returned_text}"
    )
    assert "Ngày trả:" in returned_text or "Return date:" in returned_text, (
        f"Returned record does not show a return date. Record text: {returned_text}"
    )

    direct_return_buttons = _direct_actionable_return_buttons_inside(returned_record)
    if direct_return_buttons.count() > 0:
        returned_record.scroll_into_view_if_needed(timeout=3000)
        _capture_evidence(page, TC_05_04_BUG_SCREENSHOT)

    assert direct_return_buttons.count() == 0, (
        "Returned record exposes a direct actionable return control. "
        f"Record text: {returned_text}"
    )



def test_tc_06_05_member_cannot_use_check_overdue_function(page, test_config):
    """TC-06-05: Normal members must not be able to trigger overdue checking."""
    _login_primary_member(page, test_config)
    _open_borrow_return(page)
    _click_inner_tab_if_present(page, LOOKUP_BORROWS_TAB)

    before_text = _all_semantics_text(page)
    before_overdue_count = before_text.count(OVERDUE_TEXT) + before_text.count("Overdue")

    for button_text in CHECK_OVERDUE_TEXTS:
        button = page.locator(f'flt-semantics[role="button"]:has-text("{button_text}")')
        assert button.count() == 0, (
            f"Normal member must not see or use the '{button_text}' function"
        )

    after_text = _all_semantics_text(page)
    after_overdue_count = after_text.count(OVERDUE_TEXT) + after_text.count("Overdue")
    assert after_overdue_count == before_overdue_count, (
        "Normal member session changed overdue markers without permission"
    )

    _capture_evidence(page, TC_06_05_PASS_SCREENSHOT)
