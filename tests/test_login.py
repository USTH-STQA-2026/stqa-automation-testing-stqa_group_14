
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter


def test_login_success(page, test_config):
    
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    wait_for_flutter(page, text="Đăng xuất")

   
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


def test_login_fail_wrong_password(page, test_config):
    # TODO: Students implement here (Sinh viên viết code ở đây)
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: nhập đúng email nhưng sai mật khẩu
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: chờ hệ thống phản hồi
    page.wait_for_timeout(2000)

    # [R✓] Revealability: vẫn ở trang login, KHÔNG thấy nút Đăng xuất
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" not in sem_text and "Logout" not in sem_text, \
        "Lỗi: Đăng nhập thành công dù mật khẩu sai!"


def test_login_fail_empty_fields(page, test_config):
    # TODO: Students implement here (Sinh viên viết code ở đây)
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: không nhập gì, click thẳng
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation
    page.wait_for_timeout(2000)

    # [R✓] Revealability: vẫn ở trang login
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" not in sem_text and "Logout" not in sem_text, \
        "Lỗi: Đăng nhập thành công dù để trống!"

def test_login_success_member(page, test_config):
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: nhập tài khoản member hợp lệ
    flutter_fill(page, "Email", "ba.nguyen@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation
    wait_for_flutter(page, text="Đăng xuất")

    # [R✓] Revealability: kiểm tra đăng nhập thành công
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" in sem_text or "Logout" in sem_text, \
        "Lỗi: Đăng nhập thất bại với tài khoản member!"


def test_login_fail_nonexistent_email(page, test_config):
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: nhập email không tồn tại
    flutter_fill(page, "Email", "khongtontai@gmail.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation
    page.wait_for_timeout(2000)

    # [R✓] Revealability: vẫn ở trang login, KHÔNG thấy nút Đăng xuất
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" not in sem_text and "Logout" not in sem_text, \
        "Lỗi: Đăng nhập thành công dù email không tồn tại!"
