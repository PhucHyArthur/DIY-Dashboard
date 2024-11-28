with open('backup.sql', 'r') as file:
    lines = file.readlines()

output = []
table_name = ""
columns = ""

for line in lines:
    if line.startswith('COPY'):
        # Xử lý dòng COPY để lấy tên bảng và cột
        table_info = line.strip().split(' ')[1].split('(')
        table_name = table_info[0]
        columns = table_info[1].replace(')', '').strip()  # Loại bỏ dấu đóng ngoặc
    elif line.strip() == '\\.':
        output.append(';\n')  # Kết thúc câu lệnh COPY
    elif line.strip() and not line.startswith('COPY'):
        # Xử lý dữ liệu, tránh lỗi khi có dữ liệu bị thiếu hoặc không hợp lệ
        values = line.strip().split('\t')
        # Kiểm tra nếu có giá trị bị thiếu
        values = [repr(v) if v else 'NULL' for v in values]  # Đảm bảo không có giá trị trống
        output.append(f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(values)});\n")

with open('converted.sql', 'w') as file:
    file.writelines(output)
