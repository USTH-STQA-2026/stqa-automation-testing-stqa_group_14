"""General account and UI behavior tests for logout and language switching."""
import pytest
from conftest import (
    enable_flutter_semantics, flutter_click_button,
    login, wait_for_flutter,
)


def test_logout(page, test_config):
    """TC-11: Verify a logged-in member can log out successfully.

    Precondition: Member account from test_config can log in.
    Input/Action: Click the logout control after login.
    Expected: The app returns to the login screen and shows login/email controls.
    """
    login(page, test_config)

    flutter_click_button(page, "Đăng xuất")
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng nhập" in sem_text or "Email" in sem_text, (
        "Logout failed: the login screen was not displayed after clicking Đăng xuất."
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Verify the Vietnamese UI can switch to English.

    Precondition: Member account from test_config can log in.
    Input/Action: Click the EN language button.
    Expected: Core navigation text is rendered in English, such as Logout/Borrow/Search.
    """
    login(page, test_config)

    flutter_click_button(page, "EN")
    wait_for_flutter(page, text="Logout")
    enable_flutter_semantics(page)

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(word in sem_text for word in ["Logout", "Borrow", "Search", "Library"]), (
        "Language switch failed: English UI text was not found after clicking EN."
    )
