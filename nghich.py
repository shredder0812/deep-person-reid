import requests
from bs4 import BeautifulSoup
import re

# URL được cung cấp
url = "https://onedrive.live.com/?authkey=%21AHZ%5FH345AcO7WG8&id=4E802435FFD67A52%214330860&cid=4E802435FFD67A52"

# Gửi yêu cầu GET đến URL
response = requests.get(url)

# Kiểm tra xem yêu cầu có thành công không
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tìm tất cả các liên kết trong trang
    links = soup.find_all('a', href=True)
    
    # Tạo danh sách để lưu trữ kết quả
    video_table = []
    
    # Lọc các liên kết có đuôi .mp4
    for link in links:
        href = link['href']
        if href.endswith('.mp4'):
            # Lấy tên tệp từ URL và bỏ phần .mp4
            video_name = re.search(r'[^/]+\.mp4$', href)
            if video_name:
                video_name = video_name.group(0).replace('.mp4', '')
                video_table.append((video_name, href))
    
    # In bảng kết quả
    if video_table:
        print("| Tên video        | Link dẫn đến video                       |")
        print("|------------------|------------------------------------------|")
        for name, link in video_table:
            print(f"| {name:<16} | {link:<40} |")
    else:
        print("Không tìm thấy tệp .mp4 nào trong trang.")
else:
    print(f"Không thể truy cập liên kết. Mã trạng thái: {response.status_code}")
    print("Liên kết có thể yêu cầu đăng nhập hoặc thông tin xác thực bổ sung.")