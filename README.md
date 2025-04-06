1. Công nghệ sử dụng
- Backend: Python (Flask)
- Frontend: HTML, CSS (Bootstrap)
- Lưu trữ: File JSON (giả lập database)
- Thư viện hỗ trợ:
  + hashlib: để tạo hash cho block
  + datetime: xử lý thời gian
  + random: sinh OTP
  + json: lưu chuỗi block
2. Kiến trúc hệ thống
Các thành phần chính:
- Trình duyệt người dùng (Client): nhập thông tin đăng nhập, nhập mã OTP, bình chọn.
- Flask Web Server: xử lý logic đăng nhập, xác thực OTP, ghi nhận phiếu bầu.
- Hệ thống OTP: sinh mã OTP ngẫu nhiên và xác thực.
- Blockchain Module: lưu trữ và xác minh phiếu bầu không thể chỉnh sửa.
- File JSON: giả lập nơi lưu trữ dữ liệu blockchain.
3. Hướng dẫn sử dụng hệ thống
- Giải nén project đã cung cấp
- Cài đặt Flask nếu chưa có:
     pip install flask
- Chạy ứng dụng:
     python app.py
- Mở trình duyệt và truy cập:
     http://127.0.0.1:5000
