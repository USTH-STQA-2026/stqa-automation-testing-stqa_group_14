# REPORT - STQA Library Automation Testing

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Hệ thống kiểm thử | Library Book Borrowing System - https://stqa.rbc.vn |
| Môn học | Software Testing & Quality Assurance |
| Nhóm | Group 14 |
| Công cụ | Python, pytest, Playwright |
| Công nghệ ứng dụng | Flutter Web CanvasKit |
| Nguồn yêu cầu chính | `docs/SRS-library-system.md` |
| Nguồn bối cảnh nghiệp vụ | `docs/BRD-yeu-cau-nghiep-vu.md` |
| Dữ liệu test | `docs/test-accounts.md` và seed data trong SRS |

Báo cáo này mô tả bộ automated test hiện có trong thư mục `tests/`, đối chiếu với yêu cầu trong SRS và các hướng dẫn của đề bài. Vì hệ thống dùng Flutter Web CanvasKit, các test tương tác chủ yếu qua Accessibility Semantics Tree (`flt-semantics`) thay vì DOM HTML thông thường.

## 2. Phạm vi kiểm thử

Bộ test hiện tại bao phủ các nhóm chức năng chính sau:

| Nhóm chức năng | Yêu cầu SRS liên quan | File test |
|---|---|---|
| Đăng nhập | REQ-01 | `tests/test_login.py` |
| Tìm kiếm và lọc sách | REQ-03 | `tests/test_search.py` |
| Mượn sách | REQ-04 | `tests/test_borrow_return.py` |
| Trả sách | REQ-05 | `tests/test_borrow_return.py`, `tests/test-bonus.py` |
| Xử lý quá hạn và phân quyền | REQ-06, REQ-08 | `tests/test-bonus.py` |
| Tra cứu phiếu mượn | REQ-08 | `tests/test_borrow_return.py`, `tests/test-bonus.py` |
| Đăng xuất và đổi ngôn ngữ | SRS giao diện song ngữ, chức năng chung | `tests/test_general.py` |

Ngoài 12 test case bắt buộc theo đề bài, nhóm có thêm các test mở rộng để kiểm tra case-insensitive search/filter, ràng buộc mượn sách, trạng thái thành viên, phân quyền phiếu mượn và quyền sử dụng chức năng kiểm tra quá hạn.

## 3. Môi trường và cách chạy

```bash
pip install -r requirements.txt
playwright install chromium
pytest -v
```

Cấu hình `.env` sử dụng các biến:

```env
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=ba.nguyen@email.com
TEST_PASSWORD=password123
TEST_DISPLAY_NAME=Nguyễn Học Bá
```

Một số test bonus dùng thêm biến môi trường cho tài khoản thành viên khác:

```env
MEMBER_OTHER_EMAIL=dam.tran@email.com
MEMBER_OTHER_PASSWORD=password123
MEMBER_OTHER_DISPLAY_NAME=Trần Dựa Dẫm
```

## 4. Screenshot evidence

Theo yêu cầu đề bài, mỗi test cần có screenshot minh chứng. Cơ chế hiện tại được đặt tập trung trong `conftest.py`:

| Kết quả test | Thư mục lưu screenshot |
|---|---|
| PASS | `screenshots/pass/` |
| FAIL hoặc ERROR | `screenshots/bug/` |

Tên file screenshot được sinh từ `pytest nodeid`, ví dụ:

```text
screenshots/pass/tests_test_login.py__test_login_success.png
screenshots/bug/tests_test_search.py__test_category_bar_case_insensitive.png
```

Cách này giúp tránh thiếu screenshot khi test fail trước dòng chụp ảnh, đồng thời phân loại evidence rõ ràng theo kết quả thực thi.

## 5. Danh sách test case bắt buộc

| TC | Test function | Mục tiêu | Oracle / Assertion chính |
|---|---|---|---|
| TC-01 | `test_login_success` | Đăng nhập bằng email và mật khẩu hợp lệ | Sau đăng nhập phải thấy tên người dùng hoặc nút Đăng xuất |
| TC-02 | `test_login_fail_wrong_password` | Từ chối đăng nhập khi sai mật khẩu | Không xuất hiện Đăng xuất/Logout |
| TC-03 | `test_login_fail_empty_fields` | Từ chối đăng nhập khi bỏ trống thông tin | Không xuất hiện Đăng xuất/Logout |
| TC-04 | `test_search_book_by_name` | Tìm sách theo tên với từ khóa `Flutter` | Có kết quả chứa `Flutter` |
| TC-05 | `test_search_book_no_result` | Tìm sách với từ khóa không tồn tại | Không có book card nào được hiển thị |
| TC-06 | `test_filter_by_category` | Lọc sách theo thể loại Công nghệ | Có kết quả và mọi book card đều thuộc Công nghệ |
| TC-07 | `test_search_by_author` | Tìm sách theo tác giả Nguyễn Minh Đức | Có kết quả chứa tên tác giả |
| TC-08 | `test_borrow_book` | Mượn một sách đang có sẵn | BOOK001 chuyển sang Đang mượn, có phiếu mượn, hạn trả = ngày mượn + 14 ngày |
| TC-09 | `test_view_borrowed_books` | Xem danh sách sách đang mượn | Có phiếu mượn trạng thái Đang mượn |
| TC-10 | `test_return_book` | Trả sách đang mượn | Phiếu chuyển Đã trả và sách chuyển về Có sẵn |
| TC-11 | `test_logout` | Đăng xuất khỏi hệ thống | Quay về màn hình đăng nhập, thấy Đăng nhập hoặc Email |
| TC-12 | `test_switch_language_to_english` | Chuyển giao diện sang tiếng Anh | Xuất hiện text tiếng Anh như Logout, Borrow, Search hoặc Library |

## 6. Test case mở rộng và bonus

| Test function | File | Mục tiêu | Yêu cầu / quy tắc liên quan |
|---|---|---|---|
| `test_login_success_member` | `test_login.py` | Kiểm tra đăng nhập bằng tài khoản member cụ thể | REQ-01 |
| `test_login_fail_nonexistent_email` | `test_login.py` | Kiểm tra email không tồn tại không đăng nhập được | REQ-01 |
| `test_search_bar_case_insensitive` | `test_search.py` | Kiểm tra tìm kiếm tên sách không phân biệt hoa/thường | REQ-03, BR-10 |
| `test_category_bar_case_insensitive` | `test_search.py` | Kiểm tra lọc thể loại không phân biệt hoa/thường | REQ-03, BR-10 |
| `test_borrow_exceed` | `test_borrow_return.py` | Thành viên không được mượn quá 3 sách | REQ-04, BR-01 |
| `test_suspended_borrow` | `test_borrow_return.py` | Thành viên bị tạm ngưng không được mượn sách | REQ-04, BR-03 |
| `test_expired_borrow` | `test_borrow_return.py` | Thành viên hết hạn không được mượn sách | REQ-04, BR-03 |
| `test_tc_05_05_member_cannot_return_another_members_borrowed_book` | `test-bonus.py` | Thành viên không được thấy phiếu mượn của người khác | REQ-08, BR-07 |
| `test_tc_05_04_cannot_return_book_that_is_already_returned` | `test-bonus.py` | Phiếu đã trả không được có hành động trả lại lần nữa | REQ-05 |
| `test_tc_06_05_member_cannot_use_check_overdue_function` | `test-bonus.py` | Thành viên thường không được dùng chức năng kiểm tra quá hạn | REQ-06, phân quyền vai trò |

Các test mở rộng tập trung vào negative testing và security/authorization testing. Đây là các khu vực dễ phát sinh lỗi thực tế vì liên quan đến phân quyền, trạng thái dữ liệu và ràng buộc nghiệp vụ.

## 7. Đối chiếu với SRS

| Yêu cầu SRS | Nội dung chính | Mức độ bao phủ |
|---|---|---|
| REQ-01 Login | Đăng nhập đúng, sai mật khẩu, email không tồn tại, bỏ trống | Đã kiểm thử positive và negative |
| REQ-02 View Book List | Hiển thị danh sách sách và trạng thái sách | Được kiểm tra gián tiếp qua search, borrow, return |
| REQ-03 Search & Filter | Tìm theo tên/tác giả, lọc thể loại, case-insensitive | Đã kiểm thử nhiều hướng |
| REQ-04 Borrow Book | Sách có sẵn, giới hạn 3 sách, thành viên tạm ngưng/hết hạn | Đã kiểm thử positive và negative |
| REQ-05 Return Book | Trả sách đang mượn, cập nhật trạng thái | Đã kiểm thử trả thành công và không trả phiếu đã trả |
| REQ-06 Overdue Handling | Chức năng kiểm tra quá hạn thuộc quyền thủ thư | Đã kiểm thử thành viên không được dùng chức năng này |
| REQ-07 Member Management | Thêm thành viên, validate email, trùng email | Chưa có test trực tiếp |
| REQ-08 Borrow Record Lookup | Thành viên chỉ xem phiếu của chính mình | Đã có test phân quyền ở `test-bonus.py` |

## 8. Nhận xét chất lượng test

Điểm mạnh:

- Test dùng helper trong `conftest.py` như `enable_flutter_semantics`, `flutter_fill`, `flutter_click_button`, `wait_for_flutter`, phù hợp với đặc thù Flutter CanvasKit.
- Các assertion không chỉ kiểm tra trang có load hay không, mà kiểm tra trạng thái cụ thể: text Đăng xuất, trạng thái Đang mượn/Đã trả/Có sẵn, số lượng kết quả, ngày hạn trả.
- Có nhiều negative test bám sát SRS: sai mật khẩu, email không tồn tại, bỏ trống input, vượt giới hạn mượn, thành viên bị tạm ngưng/hết hạn, phân quyền phiếu mượn.
- Screenshot được tự động hóa tập trung, tránh thiếu evidence khi test fail sớm.

Hạn chế / rủi ro:

- Một số test vẫn dùng `page.wait_for_timeout()` hoặc `time.sleep()`; theo hướng dẫn AI và assignment, nên ưu tiên `wait_for_flutter()` hoặc `locator.wait_for()` để giảm flaky test.
- REQ-07 về quản lý thành viên chưa được kiểm thử trực tiếp.
- Một số selector phụ thuộc vào text tiếng Việt trong Semantics Tree. Nếu app đổi label hoặc chuyển ngôn ngữ trước đó, test có thể fail.
- Test mượn/trả phụ thuộc seed data cụ thể như BOOK001, BOOK003, BR001, BR004. Đây là hợp lý theo SRS, nhưng cần cập nhật nếu seed data thay đổi.

## 9. Bug hoặc hành vi cần chú ý

Các test hiện tại có mục tiêu phát hiện những lỗi sau nếu hệ thống không tuân thủ SRS:

| Khu vực | Test phát hiện | Hành vi bị coi là bug |
|---|---|---|
| Search | `test_search_bar_case_insensitive` | Nhập `flutter` không tìm được sách `Flutter` |
| Filter | `test_category_bar_case_insensitive` | Nhập `công nghệ` không lọc được thể loại `Công nghệ` |
| Borrow limit | `test_borrow_exceed` | Thành viên mượn được cuốn thứ 4 |
| Member status | `test_suspended_borrow`, `test_expired_borrow` | Thành viên tạm ngưng/hết hạn vẫn mượn được sách |
| Return | `test_tc_05_04_cannot_return_book_that_is_already_returned` | Phiếu đã trả vẫn có nút Trả sách |
| Access control | `test_tc_05_05_member_cannot_return_another_members_borrowed_book` | Thành viên thấy phiếu mượn của người khác |
| Role permission | `test_tc_06_05_member_cannot_use_check_overdue_function` | Thành viên thường thấy hoặc dùng được nút Kiểm tra quá hạn |

## 10. Kết luận

Bộ test hiện tại đã bao phủ đầy đủ 12 test case bắt buộc của assignment và bổ sung thêm nhiều test mở rộng cho các quy tắc nghiệp vụ quan trọng. Các test được xây dựng dựa trên SRS, sử dụng dữ liệu seed trong tài liệu và tương tác qua Flutter Semantics Tree đúng với ràng buộc kỹ thuật của hệ thống.

Về chất lượng, bộ test có oracle tương đối mạnh vì kiểm tra trạng thái, text và dữ liệu nghiệp vụ cụ thể thay vì chỉ kiểm tra điều hướng. Điểm nên cải thiện tiếp theo là thay các chỗ chờ tĩnh bằng smart wait, bổ sung test cho REQ-07 Member Management, và nếu có thời gian thì chuyển một số nhóm dữ liệu login/search sang `pytest.mark.parametrize` để đạt bonus data-driven rõ ràng hơn.

## 11. Khai báo sử dụng AI

Nhóm có sử dụng AI/Codex để hỗ trợ rà soát yêu cầu, chuẩn hóa cơ chế screenshot và soạn thảo báo cáo. Nội dung test và nhận xét trong báo cáo đã được đối chiếu lại với SRS, BRD, tài khoản test và các file test hiện tại trong repository.
