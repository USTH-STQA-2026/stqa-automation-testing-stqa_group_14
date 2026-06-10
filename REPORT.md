# REPORT - STQA Library Automation Testing

## 1. General Information

| Item | Details |
|---|---|
| System under test | Library Book Borrowing System - https://stqa.rbc.vn |
| Course | Software Testing & Quality Assurance |
| Team | Group 14 |
| Tools | Python, pytest, Playwright |
| Application technology | Flutter Web CanvasKit |
| Main requirement source | `docs/SRS-library-system.md` |
| Business context source | `docs/BRD-yeu-cau-nghiep-vu.md` |
| Test data source | `docs/test-accounts.md` and SRS seed data |

This report summarizes the current automated test suite in the `tests/` directory and maps it to the assignment requirements and the SRS. Since the application is built with Flutter Web CanvasKit, the tests interact mainly through the Accessibility Semantics Tree (`flt-semantics`) instead of normal HTML DOM elements.

## 2. Test Scope

The current test suite covers the following functional areas:

| Functional area | Related SRS requirements | Test file |
|---|---|---|
| Login | REQ-01 | `tests/test_login.py` |
| Book search and filtering | REQ-03 | `tests/test_search.py` |
| Borrow book | REQ-04 | `tests/test_borrow_return.py` |
| Return book | REQ-05 | `tests/test_borrow_return.py`, `tests/test-bonus.py` |
| Overdue handling and authorization | REQ-06, REQ-08 | `tests/test-bonus.py` |
| Borrow record lookup | REQ-08 | `tests/test_borrow_return.py`, `tests/test-bonus.py` |
| Logout and language switching | Bilingual UI and general functions | `tests/test_general.py` |

In addition to the 12 required test cases, the suite includes extended tests for case-insensitive search/filter behavior, borrow limits, member status restrictions, borrow-record authorization, and access to the overdue-checking function.

## 3. Environment and Execution

```bash
pip install -r requirements.txt
playwright install chromium
pytest -v
```

The `.env` file uses the following variables:

```env
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=ba.nguyen@email.com
TEST_PASSWORD=password123
TEST_DISPLAY_NAME=Nguyen Hoc Ba
```

Some bonus tests also require another member account:

```env
MEMBER_OTHER_EMAIL=dam.tran@email.com
MEMBER_OTHER_PASSWORD=password123
MEMBER_OTHER_DISPLAY_NAME=Tran Dua Dam
```

## 4. Screenshot Evidence

The assignment requires every test to produce screenshot evidence. The current implementation centralizes screenshot capture in `conftest.py`.

| Test result | Screenshot folder |
|---|---|
| PASS | `screenshots/pass/` |
| FAIL or ERROR | `screenshots/bug/` |

Screenshot filenames are generated from the pytest `nodeid`, for example:

```text
screenshots/pass/tests_test_login.py__test_login_success.png
screenshots/bug/tests_test_search.py__test_category_bar_case_insensitive.png
```

This approach prevents missing evidence when a test fails before reaching a manual screenshot line, and it clearly separates passing evidence from bug/failure evidence.

## 5. Required Test Cases

| TC | Test function | Objective | Main oracle / assertion |
|---|---|---|---|
| TC-01 | `test_login_success` | Log in with a valid email and password | The user's display name or the logout control must appear |
| TC-02 | `test_login_fail_wrong_password` | Reject login with an incorrect password | The specific wrong-password error must appear and logout must not appear |
| TC-03 | `test_login_fail_empty_fields` | Reject login when both fields are empty | The required-fields error must appear and logout must not appear |
| TC-04 | `test_search_book_by_name` | Search books by name using `Flutter` | At least one result contains `Flutter` |
| TC-05 | `test_search_book_no_result` | Search with a non-existent keyword | No book card is displayed |
| TC-06 | `test_filter_by_category` | Filter books by the Technology category | Results exist and every book card belongs to Technology |
| TC-07 | `test_search_by_author` | Search books by author name | At least one result contains the target author |
| TC-08 | `test_borrow_book` | Borrow an available book | BOOK001 becomes borrowed, a borrow record is created, and due date = borrow date + 14 days |
| TC-09 | `test_view_borrowed_books` | View the list of borrowed books | A borrow record with borrowed status is visible |
| TC-10 | `test_return_book` | Return a borrowed book | The borrow record becomes returned and the book becomes available |
| TC-11 | `test_logout` | Log out of the system | The app returns to the login screen |
| TC-12 | `test_switch_language_to_english` | Switch the UI language to English | English UI text such as Logout, Borrow, Search, or Library appears |

## 6. Extended and Bonus Test Cases

| Test function | File | Objective | Related rule / requirement |
|---|---|---|---|
| `test_login_fail_nonexistent_email` | `test_login.py` | Verify that a non-existent email cannot log in | REQ-01 |
| `test_login_fail_empty_password` | `test_login.py` | Verify that login fails when password is empty | REQ-01 |
| `test_login_fail_empty_email` | `test_login.py` | Verify that login fails when email is empty | REQ-01 |
| `test_search_bar_case_insensitive` | `test_search.py` | Verify case-insensitive book search | REQ-03, BR-10 |
| `test_category_bar_case_insensitive` | `test_search.py` | Verify case-insensitive category filtering | REQ-03, BR-10 |
| `test_borrow_exceed` | `test_borrow_return.py` | Verify that a member cannot borrow more than 3 books | REQ-04, BR-01 |
| `test_suspended_borrow` | `test_borrow_return.py` | Verify that a suspended member cannot borrow books | REQ-04, BR-03 |
| `test_expired_borrow` | `test_borrow_return.py` | Verify that an expired member cannot borrow books | REQ-04, BR-03 |
| `test_tc_05_05_member_cannot_return_another_members_borrowed_book` | `test-bonus.py` | Verify that a member cannot view another member's borrow records | REQ-08, BR-07 |
| `test_tc_05_04_cannot_return_book_that_is_already_returned` | `test-bonus.py` | Verify that returned records do not expose a return action | REQ-05 |
| `test_tc_06_05_member_cannot_use_check_overdue_function` | `test-bonus.py` | Verify that normal members cannot use the overdue-checking function | REQ-06, role authorization |

The extended tests focus on negative testing and authorization testing. These areas are important because they involve role permissions, member states, and business constraints.

## 7. SRS Traceability

| SRS requirement | Main content | Coverage status |
|---|---|---|
| REQ-01 Login | Valid login, wrong password, non-existent email, empty input | Covered with positive and negative tests |
| REQ-02 View Book List | Display books and book status | Indirectly covered through search, borrow, and return tests |
| REQ-03 Search & Filter | Search by title/author, filter by category, case-insensitive behavior | Covered with multiple scenarios |
| REQ-04 Borrow Book | Available books, 3-book limit, suspended/expired member restrictions | Covered with positive and negative tests |
| REQ-05 Return Book | Return a borrowed book and update status | Covered by successful return and already-returned-record tests |
| REQ-06 Overdue Handling | Overdue checking is a librarian-only function | Covered by member authorization test |
| REQ-07 Member Management | Add member, validate email, prevent duplicate email | Not directly covered yet |
| REQ-08 Borrow Record Lookup | Members may only view their own borrow records | Covered by bonus authorization test |

## 8. Test Quality Notes

Strengths:

- The tests use project helpers such as `enable_flutter_semantics`, `flutter_fill`, `flutter_click_button`, and `wait_for_flutter`, which are appropriate for Flutter Web CanvasKit.
- Assertions check specific business outcomes instead of only checking that the page loaded.
- The suite includes meaningful negative tests: wrong password, non-existent email, empty input, borrow-limit violation, suspended/expired member restrictions, and borrow-record authorization.
- Screenshot evidence is centralized and automatically generated for both pass and failure cases.

Limitations and risks:

- Some tests still use `page.wait_for_timeout()` or `time.sleep()`. These should be replaced with `wait_for_flutter()` or `locator.wait_for()` to reduce flakiness.
- REQ-07 Member Management is not directly tested yet.
- Some locators depend on Vietnamese text in the Semantics Tree. If the app labels change, the tests may need updates.
- Borrow/return tests depend on specific seed data such as BOOK001, BOOK003, BR001, and BR004. This is acceptable for this assignment, but the tests must be updated if the seed data changes.

## 9. Potential Bugs Targeted by the Tests

The current tests are designed to expose the following defects if the system violates the SRS:

| Area | Detecting test | Defect behavior |
|---|---|---|
| Search | `test_search_bar_case_insensitive` | Input `flutter` cannot find books containing `Flutter` |
| Filter | `test_category_bar_case_insensitive` | Lowercase category input does not match the Technology category |
| Borrow limit | `test_borrow_exceed` | A member can borrow a 4th book |
| Member status | `test_suspended_borrow`, `test_expired_borrow` | Suspended or expired members can still borrow books |
| Return | `test_tc_05_04_cannot_return_book_that_is_already_returned` | A returned record still exposes a Return Book action |
| Access control | `test_tc_05_05_member_cannot_return_another_members_borrowed_book` | A member can see another member's borrow records |
| Role permission | `test_tc_06_05_member_cannot_use_check_overdue_function` | A normal member can see or use the overdue-checking function |

## 10. Conclusion

The current automated test suite covers all 12 required assignment test cases and adds several extended tests for important business rules. The tests are based on the SRS, use the documented seed data, and interact through the Flutter Semantics Tree as required by the application's technical constraints.

Overall, the suite uses reasonably strong oracles because it checks concrete UI text, business states, record visibility, and date calculations. Future improvements should include replacing static waits with smart waits, adding direct tests for REQ-07 Member Management, and converting suitable login/search scenarios to `pytest.mark.parametrize` for clearer data-driven coverage.


