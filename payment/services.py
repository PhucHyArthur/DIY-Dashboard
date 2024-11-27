# payment/services.py
from .utils import generate_transaction_ref, get_client_ip
from .vnpay_helper import VNPay 
from django.conf import settings
import datetime

def generate_vnpay_payment_url(request, client_id, order_id, amount, description, order_type='billpayment', bank_code=None):
    """
    Tạo URL thanh toán qua VNPAY dựa trên client_id và order_id.
    """
    # Tạo mã giao dịch duy nhất
    transaction_ref = generate_transaction_ref(client_id, order_id)

    # Khởi tạo đối tượng VNPay
    vnp = VNPay()
    vnp.request_data['vnp_Version'] = '2.1.0'
    vnp.request_data['vnp_Command'] = 'pay'
    vnp.request_data['vnp_TmnCode'] = settings.VNPAY['vnp_TmnCode']
    vnp.request_data['vnp_Amount'] = amount * 100  # Số tiền tính bằng đơn vị nhỏ nhất
    vnp.request_data['vnp_CurrCode'] = 'VND'
    vnp.request_data['vnp_TxnRef'] = transaction_ref
    vnp.request_data['vnp_OrderInfo'] = description
    vnp.request_data['vnp_OrderType'] = order_type
    vnp.request_data['vnp_Locale'] = 'vn'

    if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

    vnp.request_data['vnp_CreateDate'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.request_data['vnp_IpAddr'] = get_client_ip(request)
    vnp.request_data['vnp_ReturnUrl'] = settings.VNPAY['vnp_ReturnUrl']

    # Tạo URL thanh toán
    return vnp.create_payment_url(settings.VNPAY['vnp_Url'], settings.VNPAY['vnp_HashSecret'])
