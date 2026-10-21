# BÁO CÁO THỰC HÀNH SELENIUM – KIỂM THỬ TỰ ĐỘNG WEBSITE

**Sinh viên:** Lê Đình Đức Anh
**Mã sinh viên:** 23010219
**Lớp:** Đánh giá và kiểm định chất lượng phần mềm*-1-1-26(COUR01.LT2)
**Môn học:** Đánh giá và kiểm định chất lượng phần mềm*-1-1-26

## 1. Mục tiêu

- Tìm hiểu công cụ Selenium WebDriver, định vị phần tử, thao tác trình duyệt và kiểm tra kết quả.
- Xây dựng tối thiểu 5 test case kiểm thử tự động.
- Chạy test bằng Pytest, ghi nhận kết quả và lưu mã nguồn trên GitHub.

## 2. Công cụ và website được kiểm thử

- **Website:** https://www.saucedemo.com/ (website thương mại điện tử demo).
- **Ngôn ngữ:** Python 3.
- **Công cụ:** Selenium WebDriver, Pytest, Google Chrome, VS Code.
- **Tài khoản demo công khai:** `standard_user` / `secret_sauce`.
- **Tài liệu:** https://www.selenium.dev/documentation/ ; https://docs.saucelabs.com/web-apps/automated-testing/selenium/

**Nguyên lý:** Selenium WebDriver điều khiển trình duyệt Chrome, tìm phần tử bằng ID, CSS selector hoặc class, gửi dữ liệu, nhấp nút và đọc trạng thái giao diện. Pytest tổ chức và chạy các trường hợp kiểm thử; các câu lệnh `assert` đối chiếu kết quả thực tế với kết quả mong đợi.

## 3. Danh sách test case

| ID   | Nội dung         | Các bước chính                                   | Kết quả mong đợi                                                |
| ---- | ---------------- | ------------------------------------------------ | --------------------------------------------------------------- |
| TC01 | Đăng nhập hợp lệ | Nhập `standard_user` / `secret_sauce`; bấm Login | Chuyển sang `inventory.html`, hiện `Products`                   |
| TC02 | Đăng nhập sai    | Nhập mật khẩu sai; bấm Login                     | Hiện thông báo sai tài khoản/mật khẩu, không vào trang sản phẩm |
| TC03 | Thêm giỏ hàng    | Đăng nhập; thêm Sauce Labs Backpack; mở giỏ      | Badge = 1; sản phẩm xuất hiện trong giỏ                         |
| TC04 | Xóa giỏ hàng     | Đăng nhập; thêm sản phẩm; mở giỏ; xóa            | Giỏ không còn sản phẩm, badge biến mất                          |
| TC05 | Sắp xếp giá      | Đăng nhập; chọn Price (low to high)              | Giá sản phẩm tăng dần                                           |
| TC06 | Thanh toán       | Đăng nhập; thêm giỏ; nhập thông tin; hoàn tất    | Hiện `Thank you for your order!`                                |
| TC07 | Đăng xuất        | Đăng nhập; mở menu; chọn Logout                  | Trở lại màn hình đăng nhập                                      |

## 4. Cấu trúc thư mục

```text
selenium-saucedemo/
├── tests/
│   ├── conftest.py
│   └── test_saucedemo.py
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## 5. Cài đặt và chạy trên Windows (VS Code / PowerShell)

Cần cài Python 3 và Google Chrome. Mở Terminal tại thư mục dự án:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

Nếu PowerShell chặn Activate.ps1, **không cần thay đổi Execution Policy**, dùng trực tiếp:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

Selenium 4 dùng Selenium Manager để tự tìm/quản lý ChromeDriver khi phù hợp; lần đầu có thể cần Internet. Chạy từng case:

```powershell
python -m pytest tests/test_saucedemo.py::test_tc01_login_success -v
```

Chạy ẩn trình duyệt trong PowerShell:

```powershell
$env:HEADLESS="1"
python -m pytest -v
Remove-Item Env:HEADLESS
```

Lưu kết quả test thành file XML (không tự động tải lên GitHub):

```powershell
python -m pytest -v --junitxml=reports/results.xml
```

## 6. Kết quả thực nghiệm

> **Chưa xác minh trên máy của sinh viên.** Chạy test trước khi nộp, sau đó điền thông tin thật dưới đây. Không ghi PASS nếu chưa chạy.

| ID   | Kết quả thực tế | Trạng thái (PASS/FAIL) |
| ---- | --------------- | ---------------------- |
| TC01 | Chưa chạy       | Chưa xác minh          |
| TC02 | Chưa chạy       | Chưa xác minh          |
| TC03 | Chưa chạy       | Chưa xác minh          |
| TC04 | Chưa chạy       | Chưa xác minh          |
| TC05 | Chưa chạy       | Chưa xác minh          |
| TC06 | Chưa chạy       | Chưa xác minh          |
| TC07 | Chưa chạy       | Chưa xác minh          |

**Môi trường thực thi:** [Phiên bản Windows, Python, Chrome]  
**Ngày kiểm thử:** [Ngày]  
**Tổng số test PASS / FAIL:** [Điền sau khi chạy]

**Ảnh minh chứng:** [Chèn ảnh màn hình terminal Pytest hiển thị kết quả và/hoặc ảnh trình duyệt. Nếu thêm ảnh vào thư mục `screenshots/`, dùng cú pháp `![Kết quả chạy test](screenshots/ten-anh.png)` tại đây.]

## 7. Nhận xét và hạn chế

- Bộ kiểm thử bao quát các luồng cơ bản: đăng nhập, giỏ hàng, sắp xếp, thanh toán và đăng xuất.
- Mỗi test có trình duyệt riêng nhờ Pytest fixture, giúp giảm phụ thuộc giữa các test.
- Dùng `WebDriverWait` cho các bước quan trọng để hạn chế lỗi do trang chưa tải xong.
- Test phụ thuộc giao diện và dữ liệu của website demo; khi website thay đổi, locator hoặc kỳ vọng có thể cần cập nhật.
- Chưa thực hiện kiểm thử tải, bảo mật hay tương thích trên nhiều trình duyệt.

## 8. Kết luận

Bài thực hành minh họa cách sử dụng Selenium WebDriver và Pytest để kiểm thử tự động các chức năng cơ bản của một website. Việc đạt hay không đạt của từng test cần được xác nhận bằng kết quả chạy thực tế trước khi nộp.

## 9. Tài liệu tham khảo

1. Selenium Documentation: https://www.selenium.dev/documentation/
2. Selenium Manager: https://www.selenium.dev/documentation/selenium_manager/
3. Sauce Labs Selenium Guide: https://docs.saucelabs.com/web-apps/automated-testing/selenium/
