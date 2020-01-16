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


class apphandler(QABaseHandler):
    def get(self):
        action =  self.get_argument('action')
        if action == 'recommentMarket':
            """首页3个推荐位
            一般来说是指数/期货
            "symbol": "RB2005",
            "name": "螺纹2005",
            "price": 3714,
            "priceUnit": "CNY",
            "cnyPrice": 360064.91,
            "coinCnyPrice": 6.95,
            "high": 35.51000000,
            "low": 35.51000000,
            "volume": 132412,
            "amount": 7223022.64800000,
            "change": 5.93
            """
            
            pass

        elif action == 'marketlist':
            """					
            "symbol": "RB1910",
            "name": "螺纹1910",
            "price": 3714,
            "priceUnit": "CNY",
            "cnyPrice": 360064.91,
            "coinCnyPrice": 6.95,
            "high": 35.51000000,
            "low": 35.51000000,
            "volume": 132412,
            "amount": 7223022.64800000,
            "change": 5.93
            """
            pass