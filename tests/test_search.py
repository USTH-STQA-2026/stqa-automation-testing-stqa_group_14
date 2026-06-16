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
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login,
)


# Test case: Search book by name
def test_search_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    Input: Keyword "Flutter" entered in the search bar
    Output: Books with label containing "Flutter" are displayed

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

    # Wait (no more than 10 seconds for results to load)
    page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').first.wait_for(timeout=10000)

    # Assert
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    assert results.count() > 0, "No books containing 'Flutter' were found"
    

# Test case: Search book with non-existent keyword
def test_search_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    Input: Keyword "abcxyz999" entered in the search bar
    Output: No book is displayed

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

    # Wait (ensure results have loaded)
    page.wait_for_timeout(2000)

    # Assert
    books = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert books.count() == 0, f"Expected no results but found {books.count()} book(s)"


# Test case: Filter books by category
def test_filter_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    Input: "Công nghệ" entered in the category filter bar
    Output: Books belonging to "Công nghệ" category are displayed

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


# Test case: Search book by author name
def test_search_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    Input: Author name "Nguyễn Minh Đức" entered in the search bar
    Output: Books authored by "Nguyễn Minh Đức" are displayed

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
    

# Test case (bonus, data-driven): Case-insensitivity for search bar and category filter
@pytest.mark.parametrize("aria_label, keyword, expected_label", [
    ("Tìm kiếm theo tên sách hoặc tác giả...", "flutter", "Flutter"),
    ("Tìm kiếm theo tên sách hoặc tác giả...", "FLUTTER", "Flutter"),
    ("Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "công nghệ", "Công nghệ"),
    ("Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "CÔNG NGHỆ", "Công nghệ"),
], ids=["search_bar_lower", "search_bar_upper", "category_bar_lower", "category_bar_upper"])
def test_case_insensitive(page, test_config, aria_label, keyword, expected_label):
    """TC-08/09: Search bar & category filter - case-insensitive (chữ thường/hoa)

    Input: Lowercase keyword in lowercase or uppercase ("flutter"/"FLUTTER" & "công nghệ"/"CÔNG NGHỆ") entered in search bar, category filter
    Output: Books matching the keyword are displayed regardless of letter case (same results as TC-04 & TC-06)

    Steps: Log in → enter keyword into the given field → verify results still match.
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, aria_label, keyword)

    # Wait (ensure results have loaded)
    page.wait_for_timeout(2000)

    # Assert
    books = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert books.count() > 0, f"Bug: '{aria_label}' is case-sensitive — input '{keyword}' returned no results"