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


# TC-01: Verify login succeeds with valid email and password
def test_login_ok(page, test_config):
    """TC-01: Login succeeds with valid email and password (*Đăng nhập thành công với email và mật khẩu hợp lệ*)

    Description (*Mô tả*):
        Open login page → fill valid credentials → click Login →
        verify the user's display name or logout control appears.

        (*Mở trang đăng nhập → nhập thông tin hợp lệ → click Đăng nhập →
        kiểm tra tên hiển thị hoặc nút đăng xuất xuất hiện.*)

    Steps (*Các bước*):
        1. _open_login_page(page, test_config)
        2. Fill Email field with test_config["email"]
           (*Nhập Email từ test_config["email"]*)
        3. Fill Mật khẩu field with test_config["password"]
           (*Nhập Mật khẩu từ test_config["password"]*)
        4. Click "Đăng nhập" button (*Click nút "Đăng nhập"*)
        5. Wait for "Đăng xuất" text to appear (*Chờ text "Đăng xuất" xuất hiện*)
        6. Assert: display name or logout control is visible
           (*Assert: tên hiển thị hoặc nút đăng xuất có trên trang*)
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


# TC-02: Verify login fails with correct email but wrong password
def test_login_wrong_password(page, test_config):
    """TC-02: Login fails with correct email but wrong password (*Đăng nhập thất bại với email đúng nhưng sai mật khẩu*)

    Description (*Mô tả*):
        Open login page → fill valid email and an incorrect password →
        click Login → verify error message and no logout control appears.

        (*Mở trang đăng nhập → nhập email hợp lệ và mật khẩu sai →
        click Đăng nhập → kiểm tra thông báo lỗi và không có nút đăng xuất.*)

    Steps (*Các bước*):
        1. _open_login_page(page, test_config)
        2. Fill Email field with test_config["email"]
           (*Nhập Email từ test_config["email"]*)
        3. Fill Mật khẩu field with "wrongpassword"
           (*Nhập "wrongpassword" vào ô Mật khẩu*)
        4. Click "Đăng nhập" button (*Click nút "Đăng nhập"*)
        5. Assert: error "Mật khẩu không đúng" shown, no logout control
           (*Assert: hiện lỗi "Mật khẩu không đúng", không có nút đăng xuất*)
    """
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, test_config["email"])
    flutter_fill(page, PASSWORD_LABEL, "wrongpassword")
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, WRONG_PASSWORD_ERROR)


# TC-03: Verify login fails when both email and password are empty
def test_login_empty_fields(page, test_config):
    """TC-03: Login fails when both email and password are empty (*Đăng nhập thất bại khi để trống cả email và mật khẩu*)

    Description (*Mô tả*):
        Open login page → click Login without filling any field →
        verify error message and no logout control appears.

        (*Mở trang đăng nhập → click Đăng nhập mà không nhập gì →
        kiểm tra thông báo lỗi và không có nút đăng xuất.*)

    Steps (*Các bước*):
        1. _open_login_page(page, test_config)
        2. Click "Đăng nhập" button without filling any field
           (*Click nút "Đăng nhập" mà không điền thông tin*)
        3. Assert: error "Vui lòng nhập email và mật khẩu" shown, no logout control
           (*Assert: hiện lỗi "Vui lòng nhập email và mật khẩu", không có nút đăng xuất*)
    """
    _open_login_page(page, test_config)

    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)


# Extra: Verify login fails when email does not exist in the system
def test_login_unknown_email(page, test_config):
    """Extra: Login fails when email does not exist in the system (*Đăng nhập thất bại khi email không tồn tại trong hệ thống*)

    Description (*Mô tả*):
        Open login page → fill a non-existent email and any password →
        click Login → verify error message and no logout control appears.

        (*Mở trang đăng nhập → nhập email không tồn tại và mật khẩu bất kỳ →
        click Đăng nhập → kiểm tra thông báo lỗi và không có nút đăng xuất.*)

    Steps (*Các bước*):
        1. _open_login_page(page, test_config)
        2. Fill Email field with "khongtontai@gmail.com"
           (*Nhập "khongtontai@gmail.com" vào ô Email*)
        3. Fill Mật khẩu field with "password123"
           (*Nhập "password123" vào ô Mật khẩu*)
        4. Click "Đăng nhập" button (*Click nút "Đăng nhập"*)
        5. Assert: error "Không tìm thấy thành viên" shown, no logout control
           (*Assert: hiện lỗi "Không tìm thấy thành viên", không có nút đăng xuất*)
    """
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, "khongtontai@gmail.com")
    flutter_fill(page, PASSWORD_LABEL, "password123")
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, NONEXISTENT_EMAIL_ERROR)


# Extra: Verify login fails when password field is left empty
def test_login_no_password(page, test_config):
    """Extra: Login fails when password field is left empty (*Đăng nhập thất bại khi để trống mật khẩu*)

    Description (*Mô tả*):
        Open login page → fill valid email but leave password empty →
        click Login → verify error message and no logout control appears.

        (*Mở trang đăng nhập → nhập email hợp lệ nhưng để trống mật khẩu →
        click Đăng nhập → kiểm tra thông báo lỗi và không có nút đăng xuất.*)

    Steps (*Các bước*):
        1. _open_login_page(page, test_config)
        2. Fill Email field with test_config["email"]
           (*Nhập Email từ test_config["email"]*)
        3. Leave Mật khẩu field empty (*Để trống ô Mật khẩu*)
        4. Click "Đăng nhập" button (*Click nút "Đăng nhập"*)
        5. Assert: error "Vui lòng nhập email và mật khẩu" shown, no logout control
           (*Assert: hiện lỗi "Vui lòng nhập email và mật khẩu", không có nút đăng xuất*)
    """
    _open_login_page(page, test_config)

    flutter_fill(page, EMAIL_LABEL, test_config["email"])
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)


# Extra: Verify login fails when email field is left empty
def test_login_no_email(page, test_config):
    """Extra: Login fails when email field is left empty (*Đăng nhập thất bại khi để trống email*)

    Description (*Mô tả*):
        Open login page → leave email empty but fill valid password →
        click Login → verify error message and no logout control appears.

        (*Mở trang đăng nhập → để trống email nhưng nhập mật khẩu hợp lệ →
        click Đăng nhập → kiểm tra thông báo lỗi và không có nút đăng xuất.*)

    Steps (*Các bước*):
        1. _open_login_page(page, test_config)
        2. Leave Email field empty (*Để trống ô Email*)
        3. Fill Mật khẩu field with test_config["password"]
           (*Nhập Mật khẩu từ test_config["password"]*)
        4. Click "Đăng nhập" button (*Click nút "Đăng nhập"*)
        5. Assert: error "Vui lòng nhập email và mật khẩu" shown, no logout control
           (*Assert: hiện lỗi "Vui lòng nhập email và mật khẩu", không có nút đăng xuất*)
    """
    _open_login_page(page, test_config)

    flutter_fill(page, PASSWORD_LABEL, test_config["password"])
    flutter_click_button(page, LOGIN_BUTTON)

    _assert_not_logged_in(page, EMPTY_FIELDS_ERROR)

# Extra: Verify login succeeds with librarian account
def test_login_librarian(page):
    """Extra: Login succeeds with librarian account (*Đăng nhập thành công với tài khoản thủ thư*)

    Description (*Mô tả*):
        Open login page → fill librarian credentials directly →
        click Login → verify display name or logout control appears.

        (*Mở trang đăng nhập → nhập thông tin thủ thư trực tiếp →
        click Đăng nhập → kiểm tra tên hiển thị hoặc nút đăng xuất xuất hiện.*)

    Steps (*Các bước*):
        1. Navigate to "https://stqa.rbc.vn" and enable Flutter semantics
        2. Fill Email field with "librarian@library.com"
           (*Nhập "librarian@library.com" vào ô Email*)
        3. Fill Mật khẩu field with "admin123"
           (*Nhập "admin123" vào ô Mật khẩu*)
        4. Click "Đăng nhập" button (*Click nút "Đăng nhập"*)
        5. Assert: display name "Nguyễn Thủ Thư" or logout control is visible
           (*Assert: tên "Nguyễn Thủ Thư" hoặc nút đăng xuất có trên trang*)
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

