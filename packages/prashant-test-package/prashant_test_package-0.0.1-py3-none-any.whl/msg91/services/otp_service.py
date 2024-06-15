import requests

class OTPService:
    def verify_token(self, authkey, token):
        url = "https://control.msg91.com/api/v5/widget/verifyAccessToken"
        data = {
            'authkey': authkey,
            'token': token
        }
        response = requests.post(url, data=data)
        return response.json()
