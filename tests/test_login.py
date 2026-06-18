"""Login validation tests for member and librarian accounts."""

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

# Navigate to the login page and enable Flutter semantics
def _open_login_page(page, test_config):
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

# Extract all visible and aria-label text from Flutter semantics tree
def _semantics_text(page):
    enable_flutter_semantics(page)
    text_parts = page.locator("flt-semantics").all_text_contents()
    aria_parts = page.locator("flt-semantics").evaluate_all(
        "(els) => els.map((el) => el.getAttribute('aria-label') || '')"
    )
    return " ".join(text_parts + aria_parts)

# Assert that login failed: error message is shown and logout is not visible
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


def test_login_ok(page, test_config):
    """TC-01: Verify valid member credentials can log in.

    Precondition: The base URL from test_config opens the login page.
    Input/Action: Submit email and password from test_config.
    Expected: The configured display name or a logout control appears.
    """

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


def test_login_wrong_password(page, test_config):
    """TC-02: Verify login rejects an incorrect password.

    Precondition: The base URL from test_config opens the login page.
    Input/Action: Submit the configured email with password "wrongpassword".
    Expected: The wrong-password error is shown and no logout control appears.
    """
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, test_config["email"])
    flutter_fill(page, PASSWORD_LABEL, "wrongpassword")
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, WRONG_PASSWORD_ERROR)


def test_login_empty_fields(page, test_config):
    """TC-03: Verify login rejects an empty form.

    Precondition: The base URL from test_config opens the login page.
    Input/Action: Submit the login form without filling email or password.
    Expected: The required-fields error is shown and no logout control appears.
    """
    _open_login_page(page, test_config)

    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)


def test_login_unknown_email(page, test_config):
    """TC-04: Verify login rejects an email that does not exist.

    Precondition: The base URL from test_config opens the login page.
    Input/Action: Submit "khongtontai@gmail.com" with password "password123".
    Expected: The member-not-found error is shown and no logout control appears.
    """
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, "khongtontai@gmail.com")
    flutter_fill(page, PASSWORD_LABEL, "password123")
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, NONEXISTENT_EMAIL_ERROR)


def test_login_no_password(page, test_config):
    """TC-05: Verify login rejects a missing password.

    Precondition: The base URL from test_config opens the login page.
    Input/Action: Submit the configured email with an empty password field.
    Expected: The required-fields error is shown and no logout control appears.
    """
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, test_config["email"])
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)


def test_login_no_email(page, test_config):
    """TC-06: Verify login rejects a missing email.

    Precondition: The base URL from test_config opens the login page.
    Input/Action: Submit the configured password with an empty email field.
    Expected: The required-fields error is shown and no logout control appears.
    """
    _open_login_page(page, test_config)

    flutter_fill(page, PASSWORD_LABEL, test_config["password"])
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)

def test_login_librarian(page):
    """TC-07: Verify valid librarian credentials can log in.

    Precondition: The production login page is reachable.
    Input/Action: Submit librarian@library.com with password admin123.
    Expected: The librarian display name or a logout control appears.
    """
    page.goto("https://stqa.rbc.vn", wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    flutter_fill(page, EMAIL_LABEL, "librarian@library.com")
    flutter_fill(page, PASSWORD_LABEL, "admin123")
    flutter_click_button(page, LOGIN_BUTTON)

    wait_for_flutter(page, text="Đăng xuất")
    sem_text = _semantics_text(page)

    has_display_name = "Nguyễn Thủ Thư" in sem_text
    has_logout = any(text in sem_text for text in LOGOUT_TEXTS)
    assert has_display_name or has_logout, (
        "Librarian login failed: expected display name 'Nguyễn Thủ Thư' "
        f"or logout control after valid login. Actual semantics: {sem_text}"
    )

