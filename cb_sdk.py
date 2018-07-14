#/usr/bin/python3
#encoding=utf-8
import time
import hashlib
import requests
import json
import urllib
import copy
import operator
from urllib.request import urlopen, Request

class CoinBig():
		
	def __init__(self, apiKey, secret):
		self.url = 'https://www.coinbig.com/api/publics/v1'
		self.apiKey = apiKey
		self.secret = secret

	#获取账户余额	1次/1秒
	def get_balance(self):
		return self._v1('/userinfo', method='post', auth=True, apikey=self.apiKey)
		
	#获取市场深度信息	1次/1秒
	def get_depth(self, symbol):
		return self._v1('/depth?symbol=' + symbol, method='get', auth=False)
		
	#限价订单	1次/3秒
	def order_limit(self, symbol, type, price, amount):
		return self._v1('/trade', method='post', auth=True, symbol=symbol, type=type, price=price, amount=amount, apikey=self.apiKey)
	
	#市价订单	1次/3秒
	def order_market(self, symbol, type, amount):
		return self._v1('/trade', method='post', auth=True, symbol=symbol, type=type, amount=amount, apikey=self.apiKey)
	
	#查询订单状况	1次/1秒
	def order_info(self, order_id):
		return self._v1('/order_info', method='post', auth=True,  order_id=order_id, apikey=self.apiKey)
		
	#批量获取订单信息	1次/1秒	1未成交,2部分成交,3完全成交,4用户撤销,5部分撤回,6成交失败
	def orders_pending(self, symbol, type):
		return self._v1('/orders_info', method='post', auth=True, symbol=symbol, type=type, apikey=self.apiKey)	
	
	#取消订单	1次/1秒
	def cancel_order(self, order_id):
		return self._v1('/cancel_order', method='post', auth=True, order_id=order_id, apikey=self.apiKey)
		
	def _v1(self, path, method, auth, **params):
		url = self.url + path
		if auth:
			if not self.apiKey or not self.secret:
				print('API keys not configured!')
			data = self.sign(params)
		else:
			data = params
		
		if method == 'post':
			resp = self.httpPost(url, data)
		else:
			resp = self.httpGet(url)
			
		return self._process_response(resp)
			
	def _process_response(self, resp):

		data = resp
		if data['code'] != 0:
			print(data['msg'])
		return data['data']

	def sign(self, params):
		_params = copy.copy(params)
		now = int(round(time.time()))
		timeStamp = time.strftime('%Y%m%d%H%M%S',time.localtime(now))
		_params['time'] = int(timeStamp)
		sort_params = sorted(_params.items(), key=operator.itemgetter(0))
		sort_params = dict(sort_params)
		sort_params['secret_key'] = self.secret
		string = urllib.parse.urlencode(sort_params)
		_sign = hashlib.md5(bytes(string.encode('utf-8'))).hexdigest().upper()
		params['sign'] = _sign
		params['time'] = int(timeStamp)
		return params
		
	def httpGet(self,url):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		request = Request(url=url, headers=headers)
		content = urlopen(request, timeout=15).read()
		content = content.decode('utf-8')
		json_data = json.loads(content)
		return json_data

	def httpPost(self,url, params):
		temp_params = urllib.parse.urlencode(params)
		data = bytes(temp_params, encoding='utf8')
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		request = Request(url=url, data=data, headers=headers)
		content = urlopen(request).read()
		json_data = json.loads(content)
		return json_data

'''
if __name__ == '__main__':
	CB = CoinBig('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	#res1 = CB.get_depth('HT_USDT')
	#print(res1)
	#res2 = CB.get_balance()
	#print(res2)
	#res3 = CB.orders_pending('HT_USDT')
	#print(res3)
	#res4 = CB.cancel_order(61530879291376)
	#print(res4)
	#res5 = CB.order_limit('HT_USDT', 'sell', 9999, 9999)
	#print(res5)
'''
