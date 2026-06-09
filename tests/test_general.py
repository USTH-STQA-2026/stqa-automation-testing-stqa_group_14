"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
      (*Nút Đăng xuất*)
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
      (*Nút chuyển ngôn ngữ EN*)
    - After logout: page returns to login (has "Đăng nhập" button and "Email" input)
      (*Sau đăng xuất: trang quay về login*)
    - After switching to EN: text "Logout", "Borrow", "Search", "Library" may appear
      (*Sau chuyển EN: text tiếng Anh có thể xuất hiện*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_click_button,
    login, wait_for_flutter,
)


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)
    Description (*Mô tả*):
        Log in → click Logout → verify page returns to login screen.
        (*Đăng nhập → click Đăng xuất → kiểm tra quay về trang đăng nhập.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "Đăng xuất" button and click (*Tìm nút "Đăng xuất" và click*)
        3. Wait 3s, re-enable semantics (*Đợi 3s, bật lại semantics*)
        4. Assert: "Đăng nhập" button or Email input exists
           (*Assert: có nút "Đăng nhập" hoặc ô input Email*)
    """
    login(page, test_config)

    flutter_click_button(page, "Đăng xuất")
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(test_config["screenshot_dir"], "logout.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng nhập" in sem_text or "Email" in sem_text, (
        "Logout failed: the login screen was not displayed after clicking Đăng xuất."
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)
    Description (*Mô tả*):
        Log in → click "EN" button → verify UI switches to English.
        (*Đăng nhập → click nút "EN" → kiểm tra giao diện chuyển sang tiếng Anh.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "EN" button and click (*Tìm nút "EN" và click*)
        3. Wait 2s, re-enable semantics (*Đợi 2s, bật lại semantics*)
        4. Get sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
        5. Assert: "Logout" or "Borrow" or "Library" in sem_text
    """
    login(page, test_config)

    flutter_click_button(page, "EN")
    wait_for_flutter(page, text="Logout")
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(test_config["screenshot_dir"], "switch_language_to_english.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(word in sem_text for word in ["Logout", "Borrow", "Search", "Library"]), (
        "Language switch failed: English UI text was not found after clicking EN."
    )
