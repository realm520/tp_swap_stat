# -*- coding: utf-8 -*-

import json
import time
import hmac
import base64
import hashlib
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Api:

    def __init__(self, apiKey, secret):
        self.base_url = "https://api.xt.pub"
        self.apiKey = apiKey
        self.secret = secret

    def public_request(self, method, url, **payload):
        """send public request"""
        for i in range(3):
            try:
                r = requests.request(method, url, params=payload, timeout=10, verify=False)
                r.raise_for_status()
                break
            except requests.exceptions.HTTPError as err:
                print(err)
                time.sleep(1)
        if r.status_code == 200:
            return r.json()

    def signed_request(self, method, url, **payload):
        payload['accesskey'] = self.apiKey
        payload['nonce'] = str(int(time.time() * 1000))
        params = ''
        for k in sorted(payload.items()):
            params += '&' + str(k[0]) + '=' + str(k[1])
        params = params.lstrip('&')
        signature = hmac.new(self.secret.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest().upper()
        payload['signature'] = signature

        for i in range(3):
            try:
                if method == 'GET':
                    r = requests.get(url, params=payload, verify=False, timeout=10)
                else:
                    r = requests.post(url, data=payload, verify=False, timeout=10)
                r.raise_for_status()
                break
            except requests.exceptions.HTTPError as err:
                print(err)
                time.sleep(1)
        if r.status_code == 200:
            return r.json()
        else:
            return None

    def get_server_time(self):
        return self.public_request('GET', self.base_url + '/trade/api/v1/getServerTime')

    def get_account(self):
        return self.public_request('GET', self.base_url + '/trade/api/v1/getAccounts')

    def get_all_symbol(self):
        return self.public_request('GET', self.base_url + '/data/api/v1/getMarketConfig')

    def get_klines(self, market, type, since=0):
        url = self.base_url + '/data/api/v1/getKLine'
        return self.public_request('GET', url, market=market, type=type, since=since)

    def get_ticker(self, market):
        url = self.base_url + '/data/api/v1/getTicker'
        return self.public_request('GET', url, market=market)

    def get_tickers(self):
        return self.public_request('GET', self.base_url + '/data/api/v1/getTickers')

    def get_depth(self, market):
        url = self.base_url + '/data/api/v1/getDepth'
        return self.public_request('GET', url, market=market)

    def get_trades(self, market):
        url = self.base_url + '/data/api/v1/getTrades'
        return self.public_request('GET', url, market=market)

    # -----------------------   fund  -----------------------------------

    def get_fund(self):
        """ 钱包账户: 1, 交易账户: 2, 法币账户: 3 """
        return self.signed_request('GET', self.base_url + '/trade/api/v1/getFunds', account=2)

    def send_order(self, market, price, number, type, entrustType=0):
        """
        type: 1、买 0、卖
        entrustType: 0、限价，1、市价
        """
        url = self.base_url + '/trade/api/v1/order'
        return self.signed_request('POST', url, market=market, price=price, number=number, type=type, entrustType=entrustType)

    def send_orders(self, market, data):
        url = self.base_url + '/trade/api/v1/batchOrder'
        data = json.dumps(data)
        data = base64.b64encode(data.encode('utf-8'))
        return self.signed_request('POST', url, market=market, data=str(data, 'utf-8'))

    def cancel_order(self, market, id):
        url = self.base_url + '/trade/api/v1/cancel'
        return self.signed_request('POST', url, market=market, id=id)

    def cancel_orders(self, market, data):
        url = self.base_url + '/trade/api/v1/batchCancel'
        data = json.dumps(data)
        data = base64.b64encode(data.encode('utf-8'))
        return self.signed_request('POST', url, market=market, data=str(data, 'utf-8'))

    def get_order(self, market, id):
        url = self.base_url + '/trade/api/v1/getOrder'
        return self.signed_request('GET', url, market=market, id=id)

    def get_unfinished_order(self, market, page=1, pageSize=10):
        """  获取未完成订单
        page： 页码
        pageSize: 订单数量  取值范围: [10-1000]
        """
        url = self.base_url + '/trade/api/v1/getOpenOrders'
        return self.signed_request('GET', url, market=market, page=page, pageSize=pageSize)

    def get_orders(self, market, data):
        """获取多个订单信息, 订单数量  取值范围: [10-1000]"""
        url = self.base_url + '/trade/api/v1/getBatchOrders'
        data = json.dumps(data)
        data = base64.b64encode(data.encode('utf-8'))
        return self.signed_request('GET', url, market=market, data=str(data, 'utf-8'))


if __name__ == '__main__':
    api = Api('', '')
    #res = api.get_all_symbol()
    # res = api.get_klines('btc_usdt', '5min')
    # res = api.get_order('btc_sxc', 160099685172365)
    # print(api.get_depth('xwc_sxc'))
    print(api.get_ticker('xwc_sxc'))
    # print(json.dumps(res, ensure_ascii=False))
    #print(api.send_order("btc_sxc", 1, 10, 1, 0))

# 0、提交未撮合，1、未成交或部份成交，2、已完成，3、已取消，4、撮合完成结算中

