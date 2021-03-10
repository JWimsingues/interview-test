import json
import requests

import logging
import boto3
import os
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def import_intercom():
    # write your code here
    print('import_intercom')
    intercom_api_endpoint = 'https://api.intercom.io/'
    intercom_token = 'dG9rOmNkNGI3MDFiXzc3ZjJfNGQ0Ml84MWZiXzM1MDgyZDdkNmY2ZjoxOjA='

    intercom_headers = {
        'Authorization': 'Bearer ' + intercom_token,
        'Accept': 'application/json'
    }

    payload = {
        'per_page': 50
    }

    contacts_response = requests.get(intercom_api_endpoint + 'contacts', params=payload, headers=intercom_headers)
    conversations_response = requests.get(intercom_api_endpoint + 'conversations', params=payload, headers=intercom_headers)

    contacts_data = json.loads(contacts_response.content)
    conversations_data = json.loads(conversations_response.content)

    with open('contacts.json', 'w') as outfile:
        json.dump(contacts_data, outfile)

    with open('conversations.json', 'w') as outfile:
        json.dump(conversations_data, outfile)

    upload_file('contacts.json', 'nalia-technical-test', 'data/jeremy_contacts.json')
    upload_file('conversations.json', 'nalia-technical-test', 'data/jeremy_conversations.json')

    print('Cleaning env before exit...')
    os.remove('contacts.json')
    os.remove('conversations.json')

if __name__ == '__main__':
    import_intercom()