"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)

    Hints (*Gợi ý*):
        - login(page, test_config)
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
        - Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    """
    
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # Wait
    page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').first.wait_for(timeout=10000)

    # Assert
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    assert results.count() > 0, "No books containing 'Flutter' were found"
    
    # Screenshot
    page.screenshot(path=f"{test_config['screenshot_dir']}/tc04_search_by_name.png")


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)

    Hints (*Gợi ý*):
        - Verify: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "abcxyz999")

    # Wait
    page.wait_for_timeout(2000)

    # Assert
    books = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert books.count() == 0, f"Expected no results but found {books.count()} book(s)"

    # Screenshot
    page.screenshot(path=f"{test_config['screenshot_dir']}/tc05_search_no_result.png")


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    Description (*Mô tả*):
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
        (*Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách
        hiển thị đều thuộc thể loại Công nghệ.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
        - Get book list: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
          (*Lấy danh sách sách*)
        - Loop through each book, verify aria-label contains "Công nghệ"
          (*Lặp qua từng sách, kiểm tra aria-label chứa "Công nghệ"*)
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
    
    # Wait
    page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').first.wait_for(timeout=10000)

    # Assert
    books = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert books.count() > 0, "No books displayed after applying category filter"
    for i in range(books.count()):
        label = books.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label, f"Book {i+1} does not belong to 'Công nghệ': {label}"

    # Screenshot
    page.screenshot(path=f"{test_config['screenshot_dir']}/tc06_filter_by_category.png")


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
        (*Đăng nhập → tìm kiếm tên tác giả → kiểm tra có kết quả.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
        - Verify: page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")

    # Wait
    page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').first.wait_for(timeout=10000)

    # Assert
    results = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]')
    assert results.count() > 0, "No books found for author 'Nguyễn Minh Đức'"
    
    # Screenshot
    page.screenshot(path=f"{test_config['screenshot_dir']}/tc07_search_by_author.png")


def test_search_bar_case_insensitive(page, test_config):
    """TC-08: Search bar - case-insensitive (chữ thường/hoa)

    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "flutter")

    # Wait
    page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').first.wait_for(timeout=10000)

    # Assert
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    assert results.count() > 0, "Bug: search bar is case-sensitive — lowercase input returned no results"

    # Screenshot
    page.screenshot(path=f"{test_config['screenshot_dir']}/tc08_search_case_insensitive.png")


def test_category_bar_case_insensitive(page, test_config):
    """TC-09: Category bar - case-insensitive (chữ thường/hoa)
    
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "công nghệ")

    # Wait
    page.wait_for_timeout(2000)

    try:
        # Assert
        books = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
        assert books.count() > 0, "Bug confirmed: category bar is case-sensitive — lowercase input returned no results"
    finally:
        # Screenshot
        page.screenshot(path=f"{test_config['screenshot_dir']}/tc09_category_case_insensitive.png")
