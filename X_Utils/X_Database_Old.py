# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Thiết lập quyền truy cập vào Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("X_Config/google_sheets_credentials.json", scope)
client = gspread.authorize(creds)

# Mở Google Sheet của bạn bằng ID
spreadsheet_id = "1Getoqe8Gsleuo9Lu96J8FCXbzUxPHiMQoL5YbArY2_U"  # Thay thế bằng ID Google Sheets của bạn
try:
    sheet = client.open_by_key(spreadsheet_id).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    print("Google Sheets doesn't exist or the service account doesn't have access permissions. Check your ID and access rights again.")

# Thiết lập các tiêu đề cột nếu chưa có
def initialize_sheet():
    headers = ["ID Checking", "UserName", "Number of attendance times", "Detection time", "Address to save the image"]
    existing_headers = sheet.row_values(1)
    if not existing_headers:
        sheet.append_row(headers)
    elif existing_headers != headers:
        print("Warning: Existing column headings do not match expected headings. Please check Google Sheets.")

# Sử dụng bộ nhớ tạm để giảm số lần đọc từ Google Sheets
cached_user_records = None

def log_to_google_sheets(user_id, name, image_url):
    global cached_user_records

    # Kiểm tra và làm mới bộ nhớ tạm nếu cần thiết
    if cached_user_records is None:
        cached_user_records = sheet.get_all_records()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Tìm kiếm người dùng theo ID
    for index, record in enumerate(cached_user_records):
        if record.get("ID Checking") == user_id:
            # Người dùng đã tồn tại, cập nhật số lần điểm danh và thời gian phát hiện
            image_url = 'X_Image_Tracking'
            new_count = record["Number of attendance times"] + 1
            new_timestamp = f"{record['Detection time']}, {timestamp}"
            sheet.update_cell(index + 2, 3, new_count)  # Cột C: Số lần điểm danh
            sheet.update_cell(index + 2, 4, new_timestamp)  # Cột D: Thời gian phát hiện
            sheet.update_cell(index + 2, 5, image_url)  # Cột E: Địa chỉ lưu hình ảnh
            
            # Cập nhật bộ nhớ tạm
            cached_user_records[index]["Number of attendance times"] = new_count
            cached_user_records[index]["Detection time"] = new_timestamp
            cached_user_records[index]["Address to save the image"] = image_url
            return

    # Người dùng chưa tồn tại, thêm mới
    new_row = [user_id, name, 1, timestamp, image_url]
    
    # Chèn hàng mới vào vị trí thứ hai và di chuyển các hàng còn lại xuống dưới
    sheet.insert_row(new_row, 2)

    # Cập nhật bộ nhớ tạm
    cached_user_records.insert(0, {
        "ID Checking": user_id,
        "UserName": name,
        "Number of attendance times": 1,
        "Detection time": timestamp,
        "Address to save the image": image_url
    })

# Khởi tạo bảng tính
initialize_sheet()