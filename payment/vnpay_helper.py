# payment/vnpay_helper.py
import hashlib
from urllib.parse import urlencode
import urllib.parse
import hmac

class VNPay:
    request_data = {}
    responseData = {}

    def create_payment_url(self, vnpay_payment_url, secret_key):
        inputData = sorted(self.request_data.items())
        queryString = ''
        hasData = ''
        seq = 0
        for key, val in inputData:
            if seq == 1:
                queryString = queryString + "&" + key + '=' + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                queryString = key + '=' + urllib.parse.quote_plus(str(val))

        hashValue = self.__hmacsha512(secret_key, queryString)
        return vnpay_payment_url + "?" + queryString + '&vnp_SecureHash=' + hashValue

    def validate_response(self, secret_key):
    # Kiểm tra và lấy 'vnp_SecureHash' từ responseData
        vnp_SecureHash = self.responseData.get('vnp_SecureHash')
        if not vnp_SecureHash:
            raise ValueError("Missing 'vnp_SecureHash' in response data. Received: {}".format(self.responseData))

        # Loại bỏ hash params để tính toán
        self.responseData.pop('vnp_SecureHash', None)
        self.responseData.pop('vnp_SecureHashType', None)

        # Xử lý dữ liệu còn lại
        inputData = sorted(self.responseData.items())
        hasData = ''
        seq = 0
        for key, val in inputData:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    hasData = hasData + "&" + str(key) + '=' + urllib.parse.quote_plus(str(val))
                else:
                    seq = 1
                    hasData = str(key) + '=' + urllib.parse.quote_plus(str(val))

        # Tính toán hash
        hashValue = self.__hmacsha512(secret_key, hasData)
        print(
            'Validate debug, HashData:' + hasData + "\n HashValue:" + hashValue + "\nInputHash:" + vnp_SecureHash
        )
        return vnp_SecureHash == hashValue

    @staticmethod
    def __hmacsha512(key, data):
        byteKey = key.encode('utf-8')
        byteData = data.encode('utf-8')
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()
