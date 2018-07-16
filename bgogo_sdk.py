import hashlib
import urllib
import json
import time
import requests
from urllib.request import urlopen, Request

class Bgogo:
	_headers = {
		'Content-Type': 'application/json; charset=utf-8',
		'Accept': 'application/json',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
		}
		
	def __init__(self, email, password):
		self.url = 'https://www.bgogo.com/api'
		self.email = email
		self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
		self.token = self.signin()
		
	def get_version(self):
		return self.dorequest('/version', method='get', auth=False)
		'''
		Response:
		{
			status: 'ok',
			version: '1.0.0'
		}
		'''
		
	def get_balance(self):
		return self.dorequest('/balances', method='get', auth=True)
		'''
		Response:
		{
			status: 'ok',
			otp_enabled: true,
			balances: [
				{ currency: 'ETH',
				available: '0.12345600', frozen: '0.00000000', step: '0.00000001',
				deposit_enabled: true, withdraw_enabled: false },
				{ currency: 'BTC',
				available: '0.12345600', frozen: '0.00646616', step: '0.00000001',
				deposit_enabled: true, withdraw_enabled: false }
			]
		}
		'''
		
	def get_snapshot(self, symbol):		# ETH/BTC
		return self.dorequest('/snapshot/'+symbol, method='get', auth=True)
		'''
		Response:
		{
			status: 'ok',
			all_symbols: [ 'ETH/BTC', 'YANG/MEOW' ],
			last_prices: [ '0.0527', '1.00010001' ],
			past_24hrs_price_changes: [ '23.12%', '-42.40%' ],
			price_step: '0.0001',
			amount_step: '0.0001',
			order_book: {bids: [{ price: '0.0528', amount: '0.1234' },
								{ price: '0.0527', amount: '0.1234' },
								{ price: '0.0526', amount: '0.1234' },
								{ price: '0.0525', amount: '0.1234' },
								{ price: '0.0524', amount: '0.1234' }],
						asks: [{ price: '0.0529', amount: '0.1234' },
								{ price: '0.0530', amount: '0.1234' },
								{ price: '0.0531', amount: '0.1234' },
								{ price: '0.0532', amount: '0.1234' },
								{ price: '0.0533', amount: '0.1234' }] },
			trade_history: [
				{ price: '0.0528', amount: '0.1234', timestamp: 1507785073, side: 'buy' },
				{ price: '0.0528', amount: '0.1234', timestamp: 1507785072, side: 'sell' }
			],
			my_account_balances: [
				{ currency: 'ETH',available: '0.12345600', frozen: '0.00000000', step: '0.00000001' },
				{ currency: 'BTC',available: '0.12345600', frozen: '0.00646616', step: '0.00000001' }
			],
			my_orders: [
				{ id: '987654323', side: 'buy', price: '0.0524', amount: '0.1235',
				create_time: 1507785072, update_time: 1507785073, status: 'open',
				volume: '0.0001', turnover: '0.00000524' },
				{ id: '987654322', side: 'sell', price: '0.0524', amount: '0.1235',
				create_time: 1507785072, update_time: 1507785073, status: 'cancelled',
				volume: '0.0001', turnover: '0.00000524' },
				{ id: '987654321', side: 'buy', price: '0.0524', amount: '0.1235',
				create_time: 1507785072, update_time: 1507785073, status: 'closed',
				volume: '0.1235', turnover: '0.00647140' }
			],
			my_fee_rate: '0.0025'
		}
		'''
		
	def get_snapshot_unauth(self, symbol):		# ETH/BTC
		return self.dorequest('/snapshot/'+symbol, method='get', auth=False)
		'''
		Response:
		{
			status: 'ok',
			all_symbols: [ 'ETH/BTC', 'YANG/MEOW' ],
			last_prices: [ '0.0527', '1.00010001' ],
			past_24hrs_price_changes: [ '23.12%', '-42.40%' ],
			price_step: '0.0001',
			amount_step: '0.0001',
			order_book: {bids: [{ price: '0.0528', amount: '0.1234' },
								{ price: '0.0527', amount: '0.1234' },
								{ price: '0.0526', amount: '0.1234' },
								{ price: '0.0525', amount: '0.1234' },
								{ price: '0.0524', amount: '0.1234' }],
						asks: [{ price: '0.0529', amount: '0.1234' },
								{ price: '0.0530', amount: '0.1234' },
								{ price: '0.0531', amount: '0.1234' },
								{ price: '0.0532', amount: '0.1234' },
								{ price: '0.0533', amount: '0.1234' }] },
			trade_history: [
				{ price: '0.0528', amount: '0.1234', timestamp: 1507785073, side: 'buy' },
				{ price: '0.0528', amount: '0.1234', timestamp: 1507785072, side: 'sell' }
			]
		}
		'''
	
	def get_tickers(self):
		return self.dorequest('/tickers', method='get', auth=False)
		'''
		Response:
		{
			status: 'ok',
			tickers: {
				'ETH/BTC': {
					'last_price': '0.0527',
					'lowest_ask_price': '0.0400',
					'highest_bid_price': '0.0600',
					'past_24hrs_price_change': '23.12%',
					'past_24hrs_base_volume': 5.234,
					'past_24hrs_quote_turnover': 52.34,
					'past_24hrs_high_price': '0.0700',
					'past_24hrs_low_price': '0.0300'
				}
			}
		}
		'''
	
	def get_candlesticks(self, symbol, zoom, candlestick):
		return self.dorequest('/candlesticks/'+symbol+'?zoom='+str(zoom)+'&candlestick='+str(candlestick), method='get', auth=False)
		'''
		Response:
		{
			status: 'ok',
			candlesticks: [
				[1507766400, '927.7399', '949.9000', '927.7399', '944.4899', '223.940'],
				[1507852800, '941.3599', '950.6900', '940.5499', '949.5000', '102.030'],
				[1507939200, '952.0000', '959.7860', '951.5100', '959.1099', '158.100'],
				[1508025600, '959.9799', '962.5399', '947.8400', '953.2700', '128.340'],
				[1508112000, '980.0000', '987.5999', '972.2000', '972.5599', '204.214']
			]
		}
		Valid zoom & candlestick combinations:
		-------------------------------------------
		zoom    Candlestick
		-------------------------------------------
		6hr    5m  15m  30m  1hr  2hr
		24hr    5m  15m  30m  1hr  2hr  4hr
		1w         15m  30m  1hr  2hr  4hr  1d
		1m                   1hr  2hr  4hr  1d
		-------------------------------------------
		'''
	
	def order_limit(self, symbol, type, price, amount):
		return self.dorequest('place-order', method='post', auth=True, symbol=symbol, side=type, price=price, amount=amount)
		'''
		Response:
		{
			status: 'ok',
			order_id: '987654321'
		}
		'''
		
	def cancel_order(self, orderid):
		return self.dorequest('/cancel-order/'+str(orderid), method='post', auth=True)
		'''
		No response
		'''
		
	def signin(self):
		res= self.dorequest('/sign-in', method='post', auth=False, email=self.email, password=self.password)
		if res['status'] == 'error':
			if res['reason'] == 'unconfirmed device':
				print("Unconfirmed device!")
				if self.confirm_current_device():
					return self.signin()	
			else:
				print("An error occurred while sign in: ", res['reason'])			
		elif res['status'] == 'ok':
			print(" %s sign in success!"%self.email)
			return res['token']		
		else:
			if input("Unknown error! Retry? (yes/no) ") == 'yes':
				time.sleep(10)
				return self.signin()
		return ''
		
	def confirm_current_device(self):
		if not self.send_security_code():
			return 0
		security_code = input("\nPlease enter email security code:")
		otp = input("\nPlease enter Google 2FA code(if do not have, press enter):")
		if otp:
			res = self.dorequest('/confirm-current-device', method='post', auth=False, email=self.email, security_code=security_code, otp=otp, password=self.password)
		else:
			res = self.dorequest('/confirm-current-device', method='post', auth=False, email=self.email, security_code=security_code, password=self.password)		
		if res['status'] == 'ok':
			return 1
		else:
			if input("\nConfirm current device failed! Retry? (yes/no) ") == 'yes':
				time.sleep(10)
				return self.confirm_current_device()
			else:
				return 0
			
	def send_security_code(self):
		res = self.dorequest('/send-security-code', method='post', auth=False, email=self.email)
		if res['status'] == 'ok':
			print("A confirm email has been sent at ",time.strftime('%H:%M:%S',time.localtime()))
			return 1
		else:
			if input("E-mail send failed! Resend email? (yes/no) ") == 'yes':
				time.sleep(10)
				return self.send_security_code()
			else:
				return 0
		
	def dorequest(self, url, method, auth, **params):
		url = self.url + url
		headers = self._headers
		if auth:
			headers['Authorization'] = "Bearer " + self.token
		if method == 'post':
			data = json.dumps(params)
			request = requests.post(url=url, data=data, headers=headers)
			return request.json()
			
		elif method == 'get':
			request = Request(url=url, headers=headers)
			content = urlopen(request).read().decode('utf-8')
			json_data = json.loads(content)
			return json_data
			
			
if __name__ == '__main__':
	bgg = Bgogo('email', 'password')
	res0 = bgg.get_version()
	print('\n\nget_version:', res0)
	res1 = bgg.get_balance()
	print('\n\nget_balance:', res1)
	res2 = bgg.get_tickers()
	print('\n\nget_tickers:', res2)
	res3 = bgg.get_snapshot('ETH/BTC')
	print('\n\nget_snapshot:', res3)
