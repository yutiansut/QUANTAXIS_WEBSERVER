# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import os
import time

import pandas as pd
import pymongo
import random
import tornado
from tornado.iostream import StreamClosedError
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketClosedError

import QUANTAXIS as QA
from QAWebServer.basehandles import QABaseHandler, QAWebSocketHandler

"""
要实现2个api

1. SIMULATED WEBSOCKET

2. REALTIME WEBSOCKET

"""
client = set()


class INDEX(QABaseHandler):

    def get(self):
        self.render("./index.html")


class RealtimeSocketHandler(QAWebSocketHandler):
    client = set()

    def open(self):
        self.client.add(self)
        self.write_message('realtime socket start')

    def on_message(self, message):
        #assert isinstance(message,str)

        try:

            database = QA.DATABASE.get_collection(
                'realtime_{}'.format(datetime.date.today())
            )
            current = [
                QA.QA_util_dict_remove_key(item,
                                           '_id')
                for item in database.find(
                    {'code': message},
                    limit=1,
                    sort=[('datetime',
                           pymongo.DESCENDING)]
                )
            ]

            self.write_message(current[0])

        except Exception as e:
            print(e)

    def on_close(self):
        print('connection close')


class SimulateSocketHandler(QAWebSocketHandler):

    def open(self):
        self.write_message('start')

    def on_message(self, message):
        if len(str(message)) == 6:
            data = QA.QA_util_to_json_from_pandas(
                QA.QA_fetch_stock_day(
                    message,
                    '2017-01-01',
                    '2017-02-05',
                    'pd'
                )
            )
            for item in data:
                self.write_message(item)
                time.sleep(0.1)

    def on_close(self):
        print('connection close')


class MonitorSocketHandler(QAWebSocketHandler):

    def open(self):
        self.write_message('start')

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print('connection close')


class future_realtime(QABaseHandler):
    def get(self):
        """
        symbol=x&range=86400000&since=1512205140000&prevTradeTime=1512205194032

        Arguments:
            QABaseHandler {[type]} -- [description]

        """

        symbol = self.get_argument('symbol', 'RB1910')
        frequence = self.get_argument('range', '5min')

        if frequence == '86400000':
            frequence = 'day'
        elif frequence == '604800000':
            frequence = 'week'
        elif frequence == '3600000':
            frequence = '60min'
        elif frequence == '1800000':
            frequence = '30min'
        elif frequence == '900000':
            frequence = '15min'
        elif frequence == '300000':
            frequence = '5min'
        elif frequence == '60000':
            frequence = '1min'

        try:
            start = QA.QAUtil.QADate.QA_util_stamp2datetime(
                self.get_argument('since', 1512205140000))
        except:
            start = '2019-06-01'
        end = QA.QAUtil.QADate.QA_util_stamp2datetime(
            int(self.get_argument('prevTradeTime')))
        res = QA.QA_quotation(symbol, start, end, frequence, 'future_cn',
                              source=QA.DATASOURCE.MONGO, output=QA.OUTPUT_FORMAT.DATASTRUCT)
        x1 = res.data.reset_index()

        quote = QA.QA_fetch_get_future_realtime('tdx', symbol)
        x1['datetime'] = pd.to_datetime(x1['datetime'])
        x = {
            "success": True,
            "data": {
                "lines": pd.concat([x1.datetime.apply(lambda x: float(x.tz_localize('Asia/Shanghai').value/1000000)), x1.open, x1.high, x1.low, x1.close, x1.volume], axis=1).to_numpy().tolist(),
                "trades": [
                    {
                        "amount": float(quote['xianliang'].values[0]),
                        "price": float(quote['price'].values[0]),
                        "tid": 373015085,
                        "time": float(quote.index.levels[0][0].tz_localize('Asia/Shanghai').value/1000000),
                        "type": "buy"
                    }
                ],
                "depths": {
                    "asks": [
                            [
                                float(quote['ask1'].values[0]),
                                float(quote['ask_vol1'].values[0])
                            ]
                    ],
                    "bids": [
                            [
                                float(quote['bid1'].values[0]),
                                float(quote['bid_vol1'].values[0])
                            ]
                    ]
                }
            }
        }

        self.write(x)


class stock_realtime(QABaseHandler):
    def get(self):
        """
        symbol=x&range=86400000&since=1512205140000&prevTradeTime=1512205194032

        Arguments:
            QABaseHandler {[type]} -- [description]

        """

        symbol = self.get_argument('symbol', '000001')
        frequence = self.get_argument('range', '5min')

        if frequence == '86400000':
            frequence = 'day'
        elif frequence == '604800000':
            frequence = 'week'
        elif frequence == '3600000':
            frequence = '60min'
        elif frequence == '1800000':
            frequence = '30min'
        elif frequence == '900000':
            frequence = '15min'
        elif frequence == '300000':
            frequence = '5min'
        elif frequence == '60000':
            frequence = '1min'

        # with open('mock.json', 'r') as r:
        #     self.write(json.load(r))
        try:
            start = str(QA.QAUtil.QADate.QA_util_stamp2datetime(
                self.get_argument('since', 1512205140000)))
        except:
            start = '2019-08-21'
        end = str(QA.QAUtil.QADate.QA_util_stamp2datetime(
            int(self.get_argument('prevTradeTime'))))[0:19]

        #res = QA.QA_quotation(symbol, start, end, frequence, 'stock_cn','mongo', output=QA.OUTPUT_FORMAT.DATASTRUCT)
        res = QA.QA_fetch_get_stock_min('tdx', symbol, start, end, frequence)

        x1 = res

        quote = QA.QA_fetch_get_stock_realtime('tdx', symbol)
        x1['datetime'] = pd.to_datetime(x1['datetime'])
        x = {
            "success": True,
            "data": {
                "lines": pd.concat([x1.datetime.apply(lambda x: float(x.tz_localize('Asia/Shanghai').value/1000000)), x1.open, x1.high, x1.low, x1.close, x1.vol], axis=1).to_numpy().tolist(),
                "trades": [
                    {
                        "amount": float(quote['cur_vol'].values[0]),
                        "price": float(quote['price'].values[0]),
                        "tid": 373015085,
                        "time": float(quote.index.levels[0][0].tz_localize('Asia/Shanghai').value/1000000),
                        "type": ["buy", "sell"][random.randint(0, 1)]
                    }
                ],
                "depths": {
                    "asks": [
                            [
                                float(quote['ask5'].values[0]),
                                float(quote['ask_vol5'].values[0])
                            ],
                        [
                                float(quote['ask4'].values[0]),
                                float(quote['ask_vol4'].values[0])
                                ],
                        [
                                float(quote['ask3'].values[0]),
                                float(quote['ask_vol3'].values[0])
                                ],
                        [
                                float(quote['ask2'].values[0]),
                                float(quote['ask_vol2'].values[0])
                                ],
                        [
                                float(quote['ask1'].values[0]),
                                float(quote['ask_vol1'].values[0])
                                ]
                    ],
                    "bids": [
                            [
                                float(quote['bid1'].values[0]),
                                float(quote['bid_vol1'].values[0])
                            ],
                        [
                                float(quote['bid2'].values[0]),
                                float(quote['bid_vol2'].values[0])
                                ],
                        [
                                float(quote['bid3'].values[0]),
                                float(quote['bid_vol3'].values[0])
                                ],
                        [
                                float(quote['bid4'].values[0]),
                                float(quote['bid_vol4'].values[0])
                                ],
                        [
                                float(quote['bid5'].values[0]),
                                float(quote['bid_vol5'].values[0])
                                ],
                    ]
                }
            }
        }

        self.write(x)


class index_realtime(QABaseHandler):
    def get(self):
        """
        symbol=x&range=86400000&since=1512205140000&prevTradeTime=1512205194032

        Arguments:
            QABaseHandler {[type]} -- [description]

        """

        symbol = self.get_argument('symbol', '000300')
        frequence = self.get_argument('range', '5min')

        if frequence == '86400000':
            frequence = 'day'
        elif frequence == '604800000':
            frequence = 'week'
        elif frequence == '3600000':
            frequence = '60min'
        elif frequence == '1800000':
            frequence = '30min'
        elif frequence == '900000':
            frequence = '15min'
        elif frequence == '300000':
            frequence = '5min'
        elif frequence == '60000':
            frequence = '1min'

        try:
            start = QA.QAUtil.QADate.QA_util_stamp2datetime(
                self.get_argument('since', 1512205140000))
        except:
            start = '2019-06-01'
        end = QA.QAUtil.QADate.QA_util_stamp2datetime(
            int(self.get_argument('prevTradeTime')))
        res = QA.QA_quotation(symbol, start, end, frequence, 'index_cn',
                              source=QA.DATASOURCE.MONGO, output=QA.OUTPUT_FORMAT.DATASTRUCT)
        x1 = res.data.reset_index()

        quote = QA.QA_fetch_get_index_realtime('tdx', symbol)
        x1['datetime'] = pd.to_datetime(x1['datetime'])
        x = {
            "success": True,
            "data": {
                "lines": pd.concat([x1.datetime.apply(lambda x: float(x.tz_localize('Asia/Shanghai').value/1000000)), x1.open, x1.high, x1.low, x1.close, x1.volume], axis=1).to_numpy().tolist(),
                "trades": [
                    {
                        "amount": float(quote['xianliang'].values[0]),
                        "price": float(quote['price'].values[0]),
                        "tid": 373015085,
                        "time": float(quote.index.levels[0][0].tz_localize('Asia/Shanghai').value/1000000),
                        "type": "buy"
                    }
                ],
                "depths": {
                    "asks": [
                            [
                                float(quote['ask1'].values[0]),
                                float(quote['ask_vol1'].values[0])
                            ]
                    ],
                    "bids": [
                            [
                                float(quote['bid1'].values[0]),
                                float(quote['bid_vol1'].values[0])
                            ]
                    ]
                }
            }
        }

        self.write(x)



class price_realtime(QABaseHandler):
    """此函数专门为macbookpro 带Bar用户准备

    传入code/market  即可获得实时报价

    如果啥也不传入, 则给一些常见的code/market组合
    
    Arguments:
        QABaseHandler {[type]} -- [description]

    Return:
        {'code': '000001, 'price': '20.1', 'market': 'stock_cn'}
    """

    def get(self):
        code = self.get_argument('code', '000001')
        market = self.get_argument('market', 'None')

        if market == 'stock_cn':
            data = QA.QA_fetch_get_stock_realtime('tdx', code)
            return {'code': code, 'market': market, 'price': data.price.values[0]}

        elif market == 'future_cn':
            data = QA.QA_fetch_get_future_realtime('tdx', code.upper())
            return {'code': code, 'market': market, 'price': data.price.values[0]}
        elif market == 'index_cn':
            data = QA.QA_fetch_get_index_realtime('tdx', code)
            return {'code': code, 'market': market, 'price': data.price.values[0]}
        elif market == 'bond_cn':
            data = QA.QA_fetch_get_index_realtime('tdx', code)
            return {'code': code, 'market': market, 'price': data.price.values[0]}


if __name__ == '__main__':
    app = Application(
        handlers=[
            (r"/",
             INDEX),
            (r"/realtime",
             RealtimeSocketHandler),
            (r"/simulate",
             SimulateSocketHandler)
        ],
        debug=True
    )
    app.listen(8010)
    tornado.ioloop.IOLoop.instance().start()
