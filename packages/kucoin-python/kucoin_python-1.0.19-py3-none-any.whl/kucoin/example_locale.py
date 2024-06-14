from kucoin.client import Margin

client = Margin(key='65dbf24d9ab88600016b269d', secret='1394913f-3b11-4a89-bf10-bd03ce9dc07e', passphrase='Aa12345678',is_v1api=True)

#res=client.get_interest_rates("BTC")
res =client.get_repay_record(size=2)
print(res)