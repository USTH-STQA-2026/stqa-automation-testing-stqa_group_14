from conftest import (
    enable_flutter_semantics,
    flutter_click_button,
    flutter_fill,
    wait_for_flutter,
)


EMAIL_LABEL = "Email"
PASSWORD_LABEL = "Mật khẩu"
LOGIN_BUTTON = "Đăng nhập"
LOGOUT_TEXTS = ("Đăng xuất", "Logout")

WRONG_PASSWORD_ERROR = "Mật khẩu không đúng"
NONEXISTENT_EMAIL_ERROR = "Không tìm thấy thành viên"
EMPTY_FIELDS_ERROR = "Vui lòng nhập email và mật khẩu"


def _open_login_page(page, test_config):
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)


def _semantics_text(page):
    enable_flutter_semantics(page)
    text_parts = page.locator("flt-semantics").all_text_contents()
    aria_parts = page.locator("flt-semantics").evaluate_all(
        "(els) => els.map((el) => el.getAttribute('aria-label') || '')"
    )
    return " ".join(text_parts + aria_parts)


def _assert_not_logged_in(page, expected_error):
    wait_for_flutter(page, text=expected_error)
    sem_text = _semantics_text(page)

    assert expected_error in sem_text, (
        f"Expected login error '{expected_error}' was not displayed. "
        f"Actual semantics text: {sem_text}"
    )
    assert not any(text in sem_text for text in LOGOUT_TEXTS), (
        "Login should fail, but the page shows a logout control."
    )


def test_login_success(page, test_config):
    """TC-01: Login succeeds with valid email and password."""
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, test_config["email"])
    flutter_fill(page, PASSWORD_LABEL, test_config["password"])
    flutter_click_button(page, LOGIN_BUTTON)

    wait_for_flutter(page, text="Đăng xuất")
    sem_text = _semantics_text(page)

    has_user_name = test_config["display_name"] in sem_text
    has_logout = any(text in sem_text for text in LOGOUT_TEXTS)
    assert has_user_name or has_logout, (
        f"Login failed: expected display name '{test_config['display_name']}' "
        "or logout control after valid login."
    )


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fails with a valid email but wrong password."""
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, test_config["email"])
    flutter_fill(page, PASSWORD_LABEL, "wrongpassword")
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, WRONG_PASSWORD_ERROR)


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fails when both email and password are empty."""
    _open_login_page(page, test_config)

    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)


def test_login_fail_nonexistent_email(page, test_config):
    """Extra: Login fails when the email does not exist."""
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, "khongtontai@gmail.com")
    flutter_fill(page, PASSWORD_LABEL, "password123")
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, NONEXISTENT_EMAIL_ERROR)


def test_login_fail_empty_password(page, test_config):
    """Extra: Login fails when password is empty."""
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, test_config["email"])
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)


def test_login_fail_empty_email(page, test_config):
    """Extra: Login fails when email is empty."""
    _open_login_page(page, test_config)

    flutter_fill(page, PASSWORD_LABEL, test_config["password"])
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)
