#
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

APPHandler  app的对应handler



"""


class AppHandler(QABaseHandler):
    def get(self):
        action =  self.get_argument('action')

        """
        /app/market?action=recommentMarket

        /app/market?action=marketlist&
        """

        if action == 'recommentMarket':
            """首页3个推荐位
            一般来说是指数/期货

            "symbol": "RB2005",
            "name": "螺纹2005",
            "price": 3714,
            "high": 35.51000000,
            "low": 35.51000000,
            "volume": 132412,
            "amount": 7223022.64800000,
            "change": 5.93



            推荐位需要基于用户喜好/ 涨幅最高的

            QA.QA_fetch_get_index_day('tdx', '000001', QA.QA_util_get_real_date(datetime.date.today()), QA.QA_util_get_real_date(datetime.date.today()))

            {
                "result": [
                    {
                        "open": 3081.46,
                        "close": 3075.5,
                        "high": 3091.95,
                        "low": 3067.25,
                        "vol": 1903043.0,
                        "amount": 242273042432.0,
                        "up_count": 594,
                        "down_count": 932,
                        "date": "2020-01-17",
                        "code": "000001",
                        "date_stamp": 1579190400.0,
                        "volume": 1903043.0,
                        "symbol": "000001",
                        "name": "上证指数",
                        "change": -0.1934148099
                    },
                    {
                        "open": 2395.61,
                        "close": 2396.17,
                        "high": 2405.94,
                        "low": 2386.42,
                        "vol": 433493.0,
                        "amount": 80781852672.0,
                        "up_count": 0,
                        "down_count": 0,
                        "date": "2020-01-17",
                        "code": "000030",
                        "date_stamp": 1579190400.0,
                        "volume": 433493.0,
                        "symbol": "000030",
                        "name": "沪深300",
                        "change": 0.0233760921
                    },
                    {
                        "open": 3054.04,
                        "close": 3053.17,
                        "high": 3067.56,
                        "low": 3042.59,
                        "vol": 233045.0,
                        "amount": 46224605184.0,
                        "up_count": 23,
                        "down_count": 21,
                        "date": "2020-01-17",
                        "code": "000016",
                        "date_stamp": 1579190400.0,
                        "volume": 233045.0,
                        "symbol": "000016",
                        "name": "上证50",
                        "change": -0.0284868568
                    }
                ]
            }


            """
            lists = {'000001': '上证指数', '000030': '沪深300', '000016': '上证50'}
            #print(lists)
            data = pd.concat([QA.QA_fetch_get_index_day('tdx', code, QA.QA_util_get_real_date(datetime.date.today()), QA.QA_util_get_real_date(datetime.date.today())) for code in lists.keys()])
            data = data.assign(volume= data.vol, symbol= data.code, name= data.code.apply(lambda x: lists[x]), change=((data.close/data.open -1)*100).apply(lambda x: round(x,2)))

            #print(data)
            self.write({"result": QA.QA_util_to_json_from_pandas(data)})

        elif action == 'marketlist':#
            """					
            "symbol": "RB1910",
            "name": "螺纹1910",
            "price": 3714,
            "high": 35.51000000,
            "low": 35.51000000,
            "volume": 132412,
            "amount": 7223022.64800000,
            "change": 5.93



            realtime quotation 从QAREALTIME 库中拿到
            """
            codelist =  QA.QA_fetch_future_list()
            codelist = codelist[codelist.code.apply(lambda x: x.endswith('L8'))]

            lists =  codelist.set_index('code').name.to_dict()
            
            #data = pd.concat([QA.QA_fetch_get_future_day('tdx', code, QA.QA_util_get_real_date(datetime.date.today()), QA.QA_util_get_real_date(datetime.date.today())) for code in lists.keys()])
            
            
            data = data.assign(symbol= data.code, name= data.code.apply(lambda x: lists[x]), change=( data.close/data.open -1)*100)

            self.write({"result": QA.QA_util_to_json_from_pandas(data)})

        