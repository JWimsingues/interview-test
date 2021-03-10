import boto3
import datetime
import json
import mysql.connector
import os

from boto3 import client

nadiadb = mysql.connector.connect(
  host='database-2.cgvivklne8l4.eu-west-3.rds.amazonaws.com',
  user='admin',
  password='Pb81F7RFQaPHKWGnLk5q',
  database='naliatest'
)

dbcursor = nadiadb.cursor()

def clean_db():
    print('Cleaning conversation table...')
    dbcursor.execute('delete from conversation WHERE true')
    nadiadb.commit()
    print('Cleaning users table...')
    dbcursor.execute('delete from users WHERE true')
    nadiadb.commit()

def process_to_db_insert(sql_query, values):
    dbcursor.executemany(sql_query, values)
    nadiadb.commit()
    print(dbcursor.rowcount, ' line(s) inserted.')

def etl_datalake_to_datawarehouse():
    # write your code here
    print('etl_datalake_to_datawarehouse')

    print('Cleaning the tables...')
    clean_db()

    s3 = client('s3')
    bucket = 'nalia-technical-test'
    s3.download_file(bucket, 'data/jeremy_contacts.json', 'contacts.json')
    s3.download_file(bucket, 'data/jeremy_conversations.json', 'conversations.json')

    contacts = json.load(open('contacts.json', 'r'))
    conversations = json.load(open('conversations.json', 'r'))

    contacts_to_be_inserted = []
    for i in range(0, len(contacts['data'])):
        contacts_to_be_inserted.append([
            contacts['data'][i]['id'],
            contacts['data'][i]['name'],
            contacts['data'][i]['email']
        ])

    conversations_to_be_inserted = []
    for i in range(0, len(conversations['conversations'])):
        conversations_to_be_inserted.append([
            conversations['conversations'][i]['id'],
            conversations['conversations'][i]['source']['author']['id'],
            datetime.datetime.fromtimestamp(conversations['conversations'][i]['created_at']).strftime('%Y-%m-%d %H:%M:%S'),
            conversations['conversations'][i]['source']['body']
        ])


    insert_contacts_sql = 'insert into users (user_id, name, email) values (%s, %s, %s)'
    insert_conversations_sql = 'insert into conversation (conv_id, user_id, creation_date, body) values (%s, %s, %s, %s)'

    process_to_db_insert(insert_contacts_sql, contacts_to_be_inserted)
    process_to_db_insert(insert_conversations_sql, conversations_to_be_inserted)

    print('Cleaning env before exit...')
    os.remove('contacts.json')
    os.remove('conversations.json')

if __name__ == '__main__':
    etl_datalake_to_datawarehouse()
