import unittest
from msg91.services.otp_service import OTPService

class TestOTPService(unittest.TestCase):
    def setUp(self):
        self.response = None

    def test_verify_token(self):
        otp_service = OTPService()
        self.response = otp_service.verify_token('your_authkey', 'your_token')
        print("Response:", self.response)  # Print the response after calling the method

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

# run the test : python3 -m unittest tests.test_otp_service