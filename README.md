# LINKEDIN TOOL BOT GUIDE

![](https://github.com/TAHKInteractingAI/BOT_LINKEDIN/blob/main/public/DESCRIPTION_0.png)

# LƯU Ý KHI SỬ DỤNG ỨNG DỤNG
1. *Tất cả các tệp tin liên quan và tương tác với ứng dụng được lưu tại thư mục `app`.*
2. *Ứng dụng được lưu tại `app\dist\app.exe`*.
3. *Driver ứng dụng được lưu tại `app\dist\resources\chromedriver.exe`*
4. *Thư mục lưu trữ các tệp đính kèm được lưu trong `app\dist\resources\attachments`*.
5. *Tập tin phục vụ cho việc thao tác với Excel Offline được lưu tại `app\dist\resources\privates\data.xlsx`*.
6. *Ứng dụng yêu cầu với trình duyệt Chrome (126.0.6478.126) & Môi trường Internet ổn định để có thể hoạt động một cách nhanh chóng và chính xác.*
# HƯỚNG DẪN SỬ DỤNG
1. *Tải xuống với `Download ZIP` tại Github hoặc dùng lệnh sau đây với Git Bash.*

   ```bash
   git clone https://github.com/TAHKInteractingAI/BOT_LINKEDIN.git
   ```

2. *Thực hiện thao tác với dữ liệu trên Google Sheets hoặc tập tin `data.xlsx` Excel Offline và thêm các tệp đính kèm vào thư mục `attachments` (nếu có).*
3. *Khởi động ứng dụng `app.exe`.*
   - *Nhập tên tại khoản và mật khẩu LinkedIn.*
   - *Tùy chọn `Use GSheet`.*
4. *Chọn tác vụ `LOGIN` trong `Task Menu` & Nhấn nút `RUN TASK` để tiến hành đăng nhập vào website LinkedIn.*
   - *Đợi cho đến khi `Notification View` hiển thị `LOGIN SUCCESSFULLY`.*

      ![](https://github.com/TAHKInteractingAI/BOT_LINKEDIN/blob/main/public/DESCRIPTION_1.png)

   - *Trong quá trình đó, ứng dụng sẽ tiến hành kiểm tra các xác thực khi đăng nhập (nếu có) bao gồm: `PIN VERIFICATION`, `CAPTCHA` và `PHONE VERIFICATION`.*
   - *Nếu `Notification View` hiển thị bất kỳ xác thực nào với từ `DECTECTED` thì vui lòng thực hiện xác thực trong vòng `120 giây`.* ***(Vui lòng đợi đến khi có thông báo mới bắt đầu xác thực)***

      ![](https://github.com/TAHKInteractingAI/BOT_LINKEDIN/blob/main/public/DESCRIPTION_2.png)

5. *Chọn các tác vụ khác trong `Task Menu` & Nhấn nút `RUN TASK` để thực thi tác vụ.*
   - *Đợi cho đến khi 'Notification View' hiển thị `TASK COMPLETED` thì quá trình thực thi sẽ kết thúc.*

      ![](https://github.com/TAHKInteractingAI/BOT_LINKEDIN/blob/main/public/DESCRIPTION_3.png)
