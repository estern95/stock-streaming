
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
            table = soup.find('table', class_ = class_)
    except Exception as ex:
        print('Exception in get_trades')
        print(str(ex))
    finally:
        return table

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes =  bytes(key, encoding='utf-8')   #.encode('utf-8')
        value_bytes = bytes(value, encoding='utf-8') #encode('utf-8')
        
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

def publish(soup_in, topic, producer):
    response = []
    table = soup_in.find_all('tr')[1:] # remove header from list
    for trade in table:
        contract = trade.find('a',{'class' : 'Fz(s) Ell C($linkColor)'})
        last_trade_dt = trade.find('td',{'class' : 'data-col1 Ta(end) Pstart(7px)'})
        strike = trade.find('a',{'class' : 'C($linkColor) Fz(s)'})
        last_price = trade.find('td',{'class' : 'data-col3 Ta(end) Pstart(7px)'})
        bid = trade.find('td',{'class' : 'data-col4 Ta(end) Pstart(7px)'})
        ask = trade.find('td',{'class' : 'data-col5 Ta(end) Pstart(7px)'})
        change = trade.find('td',{'class' : 'data-col6 Ta(end) Pstart(7px)'})
        pct_change = trade.find('td',{'class' : 'data-col7 Ta(end) Pstart(7px)'})
        volume = trade.find('td',{'class' : 'data-col8 Ta(end) Pstart(7px)'})
        open_interest = trade.find('td',{'class' : 'data-col9 Ta(end) Pstart(7px)'})
        implied_volatility = trade.find('td',{'class' : 'data-col10 Ta(end) Pstart(7px) Pend(6px) Bdstartc(t)'})

        parsed_trade = {
            'contract' : contract,
            'last_trade_dt' : last_trade_dt,
            'strike' : strike,
            'last_price' : last_price,
            'bid' : bid,
            'ask' : ask,
            'change' : change,
            'pct_change' : pct_change,
            'volume' : volume,
            'open_interest' : open_interest,
            'implied_volatility' : implied_volatility
        }

        for key, obs in parsed_trade.items():
            try:
                parsed_trade[key] = obs.text.strip()
            except:
                print('fail to parse observation {}', obs)
                parsed_trade[key] = ''

        publish_message(producer, topic, 'clean', json.dumps(parsed_trade))


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
        kafka_producer = connect_kafka_producer()
        calls = get_trades(class_ = calls_class)
        publish(calls, 'TSLA_calls', kafka_producer)

        puts = get_trades(class_ = puts_class)
        publish(puts, 'TSLA_puts', kafka_producer)
        kafka_producer.close()
        ix += 1
        
        sleep(10)