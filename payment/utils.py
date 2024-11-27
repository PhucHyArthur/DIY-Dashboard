# payment/utils.py
import uuid
import hashlib

def generate_transaction_ref(client_id, order_id):
    """
    Tạo mã giao dịch duy nhất từ client_id và order_id.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{client_id}-{order_id}"))


def get_client_ip(request):
    """
    Lấy địa chỉ IP của client từ request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_secure_hash(data, secret_key):
    """
    Tạo chữ ký bảo mật từ dữ liệu và khóa bí mật.
    """
    # Sắp xếp tham số theo thứ tự bảng chữ cái
    sorted_data = sorted(data.items())
    
    # Nối các tham số theo định dạng key=value và dùng '&' để nối giữa các cặp key-value
    hash_data = '&'.join([f"{k}={v}" for k, v in sorted_data])
    
    # Tạo hash SHA256 từ chuỗi tham số và secret key
    secure_hash = hashlib.sha256((secret_key + hash_data).encode('utf-8')).hexdigest()
    return secure_hash