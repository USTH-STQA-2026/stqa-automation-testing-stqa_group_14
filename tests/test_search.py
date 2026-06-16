"""Search and filter tests for the library book catalog."""
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, wait_for_flutter,
)


NO_RESULT_TEXT = "Không tìm thấy sách"


def _book_cards(page):
    return page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')


def _wait_for_books_or_empty_state(page, timeout=10000):
    page.locator(
        f'flt-semantics[role="group"][aria-label*="Mã: BOOK"], '
        f'flt-semantics:has-text("{NO_RESULT_TEXT}"), '
        f'flt-semantics[aria-label*="{NO_RESULT_TEXT}"]'
    ).first.wait_for(state="attached", timeout=timeout)


def test_search_name(page, test_config):
    """TC-04: Verify searching by book title returns matching books.

    Precondition: Member account from test_config can log in.
    Input/Action: Enter keyword "Flutter" in the book/author search field.
    Expected: At least one displayed book contains "Flutter" in its semantics label.
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
    

def test_search_no_result(page, test_config):
    """TC-05: Verify unknown search keywords show the no-result message.

    Precondition: Member account from test_config can log in.
    Input/Action: Enter keyword "abcxyz999" in the book/author search field.
    Expected: The no-result message is shown and no book card remains visible.
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "abcxyz999")

    # Wait
    wait_for_flutter(page, text=NO_RESULT_TEXT)

    # Assert
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert NO_RESULT_TEXT in sem_text, (
        f"Expected no-result message '{NO_RESULT_TEXT}' was not displayed."
    )
    books = _book_cards(page)
    assert books.count() == 0, f"Expected no results but found {books.count()} book(s)"


def test_filter_category(page, test_config):
    """TC-06: Verify filtering by category returns only matching books.

    Precondition: Member account from test_config can log in.
    Input/Action: Enter category keyword "C?ng ngh?" in the category filter field.
    Expected: At least one book is shown and every visible book belongs to that category.
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


def test_search_author(page, test_config):
    """TC-07: Verify searching by author name returns matching books.

    Precondition: Member account from test_config can log in.
    Input/Action: Enter "Nguy?n Minh ??c" in the book/author search field.
    Expected: At least one displayed result contains that author in the semantics label.
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
    

@pytest.mark.parametrize("aria_label, keyword, expected_label", [
    ("Tìm kiếm theo tên sách hoặc tác giả...", "flutter", "Flutter"),
    ("Tìm kiếm theo tên sách hoặc tác giả...", "FLUTTER", "Flutter"),
    ("Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "công nghệ", "Công nghệ"),
    ("Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "CÔNG NGHỆ", "Công nghệ"),
], ids=["search_bar_lower", "search_bar_upper", "category_bar_lower", "category_bar_upper"])
def test_case_insensitive(page, test_config, aria_label, keyword, expected_label):
    """TC-08/09: Verify search and category filters ignore letter case.

    Precondition: Member account from test_config can log in.
    Input/Action: Enter parametrized lowercase/uppercase title or category keywords.
    Expected: Matching book cards are still displayed for every keyword variant.
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, aria_label, keyword)

    # Wait
    _wait_for_books_or_empty_state(page)

    # Assert
    books = _book_cards(page)
    assert books.count() > 0, f"Bug: '{aria_label}' is case-sensitive — input '{keyword}' returned no results"
