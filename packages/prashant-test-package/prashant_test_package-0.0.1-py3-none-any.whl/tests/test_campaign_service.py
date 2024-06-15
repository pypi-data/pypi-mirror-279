import unittest
from msg91.services.campaign_service import CampaignService

class TestOTPService(unittest.TestCase):
    def setUp(self):
        self.response = None

    def test_verify_token(self):
        cs = CampaignService('362701AThJXZtEkJd66597be2P1')
        input_data = {
    'data': [
        {
            "to": "prashant@walkover.in",
            "cc": "prashant@walkover.in",
            "bcc": "prashant@walkover.in",
            'mobiles': '919165174704',
            "name": 'prashant',
            "from_name": "prashant",
            "from_email": "prashant@walkover.in",
            "variables": {
                "var1": "1",
                "var2": "2",
            }
        },
        {
            'to': "harshjaiswal@whozzat.com",
            "cc": "harshjaiswal@whozzat.com",
            "bcc": "harshjaiswal@whozzat.com",
            'mobiles': '9111145351',
            "from_name": "harsh",
            "from_email": "harshjaiswal@whozzat.com"
        }
    ],
    "reply_to": [
        {
            'name': 'harsh',
            'email': 'prashant@walkover.in'
        }
    ]
}
        self.response = cs.run_campaign('mahenderwalkover', input_data)
        print("Response:", self.response)  # Print the response after calling the method

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()


# run the test : python3 -m unittest tests.test_campaign_service