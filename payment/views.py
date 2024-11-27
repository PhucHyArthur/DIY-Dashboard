# payment/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer
from .services import generate_vnpay_payment_url
from .models import Payment
from .utils import generate_secure_hash
from django.conf import settings
from .vnpay_helper import VNPay

class CreatePaymentView(APIView):
    def post(self, request):
        """
        API để tạo URL thanh toán VNPAY.
        """
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Lấy dữ liệu đã xác thực
        data = serializer.validated_data
        client_id = data['client_id']
        order_id = data['order_id']
        amount = data['amount']
        description = data['description']

        # Kiểm tra nếu đơn hàng đã tồn tại
        if Payment.objects.filter(order_id=order_id).exists():
            return Response({'error': 'Order ID already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo URL thanh toán
        payment_url = generate_vnpay_payment_url(
            request=request,
            client_id=client_id,
            order_id=order_id,
            amount=amount,
            description=description,
            order_type='billpayment',
            bank_code=None
        )

        # Lưu thông tin giao dịch vào cơ sở dữ liệu
        Payment.objects.create(
            client_id=client_id,
            order_id=order_id,
            amount=amount,
            description=description
        )

        return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)

class PaymentReturnView(APIView):
    def get(self, request):
        """
        Xử lý phản hồi từ VNPAY khi giao dịch hoàn tất.
        """
        print("Request GET Data:", request.GET)
        input_data = request.query_params  # Lấy dữ liệu từ query string
        if not input_data:
            return Response({"title": "Kết quả thanh toán", "result": ""}, status=status.HTTP_400_BAD_REQUEST)

        # Khởi tạo VNPay Helper
        vnpay = VNPay()
        vnpay.responseData = request.GET.dict()
        print("Response Data:", vnpay.responseData)

        # Trích xuất thông tin từ phản hồi
        order_id = input_data.get('vnp_TxnRef')
        amount = int(input_data.get('vnp_Amount', 0)) / 100  # Chuyển đổi về đơn vị tiền tệ thực
        order_desc = input_data.get('vnp_OrderInfo')
        vnp_TransactionNo = input_data.get('vnp_TransactionNo')
        vnp_ResponseCode = input_data.get('vnp_ResponseCode')
        vnp_TmnCode = input_data.get('vnp_TmnCode')
        vnp_PayDate = input_data.get('vnp_PayDate')
        vnp_BankCode = input_data.get('vnp_BankCode')
        vnp_CardType = input_data.get('vnp_CardType')

        # Xác thực chữ ký bảo mật
        if vnpay.validate_response(settings.VNPAY['vnp_HashSecret']):
            if vnp_ResponseCode == "00":
                # Giao dịch thành công
                return Response({
                    "title": "Kết quả thanh toán",
                    "result": "Thành công",
                    "order_id": order_id,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": vnp_TransactionNo,
                    "vnp_ResponseCode": vnp_ResponseCode,
                }, status=status.HTTP_200_OK)
            else:
                # Giao dịch thất bại
                return Response({
                    "title": "Kết quả thanh toán",
                    "result": "Lỗi",
                    "order_id": order_id,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": vnp_TransactionNo,
                    "vnp_ResponseCode": vnp_ResponseCode,
                }, status=status.HTTP_200_OK)
        else:
            # Sai chữ ký bảo mật
            return Response({
                "title": "Kết quả thanh toán",
                "result": "Lỗi",
                "order_id": order_id,
                "amount": amount,
                "order_desc": order_desc,
                "vnp_TransactionNo": vnp_TransactionNo,
                "vnp_ResponseCode": vnp_ResponseCode,
                "msg": "Sai checksum",
            }, status=status.HTTP_400_BAD_REQUEST)
