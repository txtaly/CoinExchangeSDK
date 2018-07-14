#encoding=utf-8
import requests
import hashlib
import time
class AllCoin():
	def __init__(self, api_key, secret):
		self.base_url = 'https://www.allcoin.com'
		self.api_key = api_key
		self.secret = secret

	def getbalance(self):
		url = '/Api_User/userBalance'
		params = {'api_key':self.api_key}
		return self.sign_requests(auth=True, method='post', api_url=url, params=params)

	def cancel(self,order_id,symbol):
		url = '/Api_Order/cancel'
		params = {'api_key':self.api_key,'symbol':symbol,'order_id':order_id}
		return self.sign_requests(auth=True, method='post', api_url=url, params=params)

	def buy(self,symbol,price,number):
		url = '/Api_Order/coinTrust'
		params = {'api_key':self.api_key,'symbol':symbol,'type':'buy','price':price,'number':number}
		return self.sign_requests(auth=True, method='post', api_url=url, params=params)

	def sell(self,symbol,price,number):
		url = '/Api_Order/coinTrust'
		params = {'api_key':self.api_key,'symbol':symbol,'type':'sell','price':price,'number':number}
		return self.sign_requests(auth=True, method='post', api_url=url, params=params)

	def depth(self,symbol):   
		url = '/Api_Order/depth'
		params = {'symbol':symbol}
		return self.sign_requests(auth=False, method='post', api_url=url, params=params)

	def order_pending(self, symbol):
		url = '/Api_Order/tradeList'
		params = {'api_key': self.api_key, 'symbol': symbol, 'type': 'open'}
		return self.sign_requests(auth=True, method='post', api_url=url, params=params)
		


	def _sign(self,params):
		data = '&'.join([key + '=' + str(params[key]) for key in sorted(params)])
		data = data + '&secret_key=' + self.secret
		data = data.encode()
		return hashlib.md5(data).hexdigest()

	def sign_requests(self, auth, method, api_url, params):
		url = self.base_url+api_url

		if auth:
			sign = self._sign(params)
			params.update(sign=sign)

		if method=='post':
			try:
				r = requests.post(url=url, data=params)
				r.raise_for_status()
			except requests.exceptions.HTTPError as err:
				print(err)
				print(r.text)
			if r.status_code == 200:
				return r.json()
