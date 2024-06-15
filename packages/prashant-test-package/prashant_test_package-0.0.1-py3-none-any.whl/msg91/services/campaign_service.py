import requests
import re

class CampaignService:
    BASE_URL = 'https://control.msg91.com/api/v5/campaign/api/'

    def __init__(self, auth_key):
        self.auth_key = auth_key

    def run_campaign(self, campaign_slug, input_data):
        self.verify_input_data(input_data)
        mapping_data = self.verify_and_get_campaign_mappings(campaign_slug)
        send_campaign = {'data': self.create_send_to_body(input_data, mapping_data)}
        self.send_campaign(campaign_slug, send_campaign)
        return "Campaign Run Successfully"

    def verify_input_data(self, input_data):
        if not input_data or len(input_data) == 0:
            raise ValueError("Must require a record to Run Campaign")
        if len(input_data) > 1000:
            raise ValueError("Record data limit exceeded: total limit 1000")

    def verify_and_get_campaign_mappings(self, campaign_slug):
        operation = f'campaigns/{campaign_slug}/fields?source=launchCampaign'
        campaign_mappings = self.make_api_call(operation)

        if 'mapping' not in campaign_mappings or not campaign_mappings['mapping']:
            raise ValueError("Invalid Campaign or no Node in Campaign")

        mapping_data = {
            'mappings': [mapping['name'] for mapping in campaign_mappings['mapping']],
            'variables': campaign_mappings.get('variables', [])
        }
        return mapping_data

    def create_send_to_body(self, input_data, mapping_data):
        send_campaign = []
        mappings = mapping_data['mappings']
        variables = mapping_data['variables']

        for data in input_data['data']:
            temp = {}

            for map in mappings:
                if map in data:
                    if map == 'to' and self.is_valid_email(data[map]):
                        temp[map] = [{'email': data[map]}]
                    elif map == 'mobiles' and self.is_valid_mobile(data[map]):
                        temp.setdefault('to', [{}])[0]['mobiles'] = data[map]
                    elif map in ['cc', 'bcc'] and self.is_valid_email(data[map]):
                        temp[map] = [{'email': data[map]}]
                    elif map == 'from_name':
                        temp[map] = data[map]
                    elif map == 'from_email' and self.is_valid_email(data[map]):
                        temp[map] = data[map]

            if 'to' in data and 'name' in data and data['name']:
                temp.setdefault('to', [{}])[0]['name'] = data['name']

            temp['variables'] = {var: data['variables'][var] for var in variables if var in data.get('variables', {})}

            send_campaign.append(temp)

        send_to_body = {'sendTo': send_campaign}
        if 'reply_to' in input_data:
            send_to_body['reply_to'] = input_data['reply_to']
        if 'attachments' in input_data:
            send_to_body['attachments'] = input_data['attachments']

        return send_to_body

    def send_campaign(self, campaign_slug, data):
        operation = f'campaigns/{campaign_slug}/run'
        self.make_api_call(operation, data, 'POST')

    def make_api_call(self, operation, input_data=None, method='GET'):
        headers = {'authkey': self.auth_key}
        url = self.BASE_URL + operation

        if method == 'POST':
            response = requests.post(url, json=input_data, headers=headers)
        else:
            response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"API call failed: {response.text}")

        return response.json()['data']

    def is_valid_email(self, email):
        regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(regex, email) is not None

    def is_valid_mobile(self, mobile):
        regex = r'^\+?[0-9]{7,14}$'
        return re.match(regex, mobile) is not None
