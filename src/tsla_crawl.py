
from __future__ import unicode_literals
import json
from time import sleep

from bs4 import BeautifulSoup
from kafka import KafkaConsumer, KafkaProducer
import requests

# -*- coding: utf-8 -*-
calls_class = 'calls W(100%) Pos(r) Bd(0) Pt(0) list-options'
puts_class = 'puts W(100%) Pos(r) list-options'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache'
    }

        
def get_trades(class_,
               base_url = 'https://finance.yahoo.com/quote/TSLA/options?straddle=false'):
    url = base_url
    print('Accessing list')

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find_all('table', class_ = class_)[0] # Grab the first table
    except Exception as ex:
        print('Exception in get_trades')
        print(str(ex))
    finally:
        return table

def publish_message(producer_instance, topic_name, key, value):
    try:
        #print(key)
        #print(value)
        key_bytes =  bytes(key, encoding='utf-8')   #.encode('utf-8')
        value_bytes = bytes(value, encoding='utf-8') #encode('utf-8')
        
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

def connect_kafka_producer(server_address = ['localhost:9092']):
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers = server_address, api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__ == "__main__":
    ix = 0

while True:
    print('Scraping...')
    if ix == 10:
        print('Exiting')
        break
    calls = get_trades(class_ = calls_class)
    kafka_producer = connect_kafka_producer()
    publish_message(kafka_producer, 'TSLA_calls', 'raw', str(calls))
    kafka_producer.close()

    puts = get_trades(class_ = puts_class)
    kafka_producer = connect_kafka_producer()
    publish_message(kafka_producer, 'TSLA_puts', 'raw', str(puts))
    kafka_producer.close()
    ix += 1
    sleep(10)