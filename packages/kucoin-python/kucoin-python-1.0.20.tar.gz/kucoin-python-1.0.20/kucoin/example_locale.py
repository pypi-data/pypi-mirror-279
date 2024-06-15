import time

from kucoin.client import Margin, Trade, Lending

def test_Trade():
    client = Trade(key='', secret='', passphrase='')
    #res=client.get_interest_rates("BTC")
    res =client.create_market_order(symbol='FRM-USDT',side='buy',clientOid=f'clientid-{time.time()*1000}',size=5)
    print(res)

def test_Lending():
    client2 = Lending(key='', secret='', passphrase='')
    res= client2.get_currency_information(currency='BTC')
    print(res)


