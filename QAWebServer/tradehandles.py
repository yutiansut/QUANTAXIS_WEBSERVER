#coding :utf-8
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
import json
import pandas as pd
import tornado
import pymongo
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler
from QUANTAXIS.QAARP import QA_Account, QA_Portfolio, QA_User
from QAWebServer.basehandles import QABaseHandler, QAWebSocketHandler
from QUANTAXIS.QAMarket.QAShipaneBroker import QA_SPEBroker
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION, ORDER_STATUS, ORDER_MODEL, AMOUNT_MODEL
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas
"""
GET http://localhost:8888/accounts
GET http://localhost:8888/positions
GET http://localhost:8888/orders
POST http://localhost:8888/orders
DELETE http://localhost:8888/orders/O1234
GET http://localhost:8888/clients
"""
""" 
心跳包断线重连 ( EXAMPLE 拔网线等直接导致的网络中断)
http://www.voidcn.com/article/p-zshodvff-mm.html

Returns:
    [type] -- [description]
"""


class TradeInfoHandler(QABaseHandler):
    """trade 信息查询句柄

    Arguments:
        QABaseHandler {[type]} -- [description]

    ?func=ping  ping 服务器
    ?func=clients 查询当前的可用客户端
    ?func=accounts 查询当前的账户
    ?func=positions&account=xxx 查询账户持仓
    ?func=orders&status 查询订单

    下单/撤单功能不在此handler提供
    """

    broker = QA_SPEBroker()

    def funcs(self, func, account, *args, **kwargs):
        if func == 'ping':
            data = self.broker.query_clients()
            return data
        elif func == 'clients':
            data = self.broker.query_clients()
            return data
        elif func == 'accounts':
            data = self.broker.query_accounts(account)
            return data
        elif func == 'positions':
            data = self.broker.query_positions(account)
            if isinstance(data, dict):
                data['hold_available'] = data['hold_available'].to_dict()
            return data
        elif func == 'orders':
            status = self.get_argument('status', '')
            return self.broker.query_orders(account, status)

        elif func == 'cancel_order':
            orderid = self.get_argument('orderid')
            return self.broker.cancel_order(account, orderid)

    def get(self):
        func = self.get_argument('func', 'ping')
        account = self.get_argument('account', None)
        print(account)
        print(func)
        data = self.funcs(func, account)
        print(data)
        if isinstance(data, pd.DataFrame):
            self.write({'result': QA_util_to_json_from_pandas(data)})
        else:
            self.write({'result': data})


null = None


class AccModelHandler(QAWebSocketHandler):
    port = QA_Portfolio(portfolio_cookie='trade_special')
    broker = [
        'haitong',
        'ths_moni',
        'tdx_moni',
        'quantaxis_backtest',
        'ctp',
        'ctp_min'
    ]
    Broker = QA_BacktestBroker()
    systime = False

    def open(self):
        self.write_message(
            {
                'data': 'QUANTAXIS BACKEND: realtime socket start',
                'topic': 'open',
                'mes': 'QUANTAXIS BACKEND: realtime socket start',
                'status': 200
            }
        )

    def on_message(self, message):
        """
        返回值需要带上
        1. topic
        2. status
        3. mes 用于客户端记录log
        """
        try:
            message = eval(message)

            # self.write_message({'topic':'receive', 'status': 304, 'input_param': message})
            if message['topic'] == 'query':
                """
                {
                    'topic' : 'query',
                    'subtopic': 'xxxx',
                }
                """

                if message['subtopic'] == 'portfolio':
                    self.write_message(
                        {
                            'topic': 'query_portfolio',
                            'status': 200,
                            'mes': 'QAT: get_query_portfolio',
                            'result': list(self.port.accounts.keys()),
                        }
                    )
                elif message['subtopic'] == 'history':
                    self.write_message(
                        {
                            'topic':
                            'history',
                            'status':
                            200,
                            'mes':
                            'QAT: get_query_history',
                            'data':
                            self.port.get_account_by_cookie(
                                message['account_cookie']
                            ).history
                        }
                    )
                elif message['subtopic'] == 'filled_order':
                    self.write_message(
                        {
                            'topic': 'filled_orders',
                            'mes': 'QAT: get_filled_order_query',
                            'status': 200
                        }
                    )
                elif message['subtopic'] == 'available_account':
                    self.write_message(
                        {
                            'status': 200,
                            'topic': 'query_account',
                            'mes': 'QAT: get_query_account_command',
                            'data': list(self.port.accounts.keys())
                        }
                    )
                elif message['subtopic'] == 'info':
                    ac = self.port.get_account_by_cookie(
                        message['account_cookie']
                    )
                    self.write_message(
                        {
                            'topic':
                            'account_info',
                            'status':
                            200,
                            'data': {
                                'hold': ac.hold.to_dict(),
                                'cash': ac.cash_available
                            },
                            'mes':
                            'QAT: get account {} info successfully'.format(
                                ac.account_cookie
                            )
                        }
                    )
            elif message['topic'] == 'login':
                """
                login$account$broker$password$tpassword$serverip

                """

                account, broker, password, tpassword, serverip = message[
                    'account_cookie'], message['broker'], message['password'], message['tpassword'], message['server_ip']

                if broker == 'quantaxis_backtest':
                    self.account = self.port.new_account(account_cookie=account)
                    print(self.account.account_cookie)

                    z = {
                        'topic':
                        'login',
                        'status':
                        200,
                        'account_cookie':
                        self.account.account_cookie,
                        'mes':
                        'QAT: success login QUANTAXIS_BACKTEST  welcome {}'
                        .format(self.account.account_cookie)
                    }
                    print(z)
                    self.write_message(z)
                    print('fin write')
                elif broker in ['ths_moni', 'tdx_moni']:
                    self.account = self.port.new_account(account_cookie=account)
                elif broker in ['simnow']:

                    pass

            elif message['topic'] == 'trade':
                """account/code/price/amount/towards/time

                先给个简易版本

                websocket 请求
                {
                'topic': 'trade',
                'code' : code,
                'account': xxxx,
                'price': price,
                'amount' : amount,
                'time' : time,
                'towards': towards
                }

                topic: trade
                status: 200/304/404/500
                mes: xxxx
                data: xxxx

                """
                self.write_message(
                    {
                        'topic':
                        'mes',
                        'status':
                        200,
                        'mes':
                        'QAtrader:get_{}_{}_{}_{}_{}'.format(
                            message['account'],
                            message['code'],
                            message['price'],
                            message['amount'],
                            message['time']
                        )
                    }
                )
                ac = self.port.get_account_by_cookie(message['account'])
                self.systime = self.systime if self.systime else str(
                    message['time']
                )
                if self.systime < str(message['time']):
                    ac.settle()

                order = ac.send_order(
                    code=str(message['code']),
                    time=str(message['time']),
                    amount=int(message['amount']),
                    towards=int(message['towards']),
                    price=float(message['price']),
                    order_model=ORDER_MODEL.MARKET,
                    amount_model=AMOUNT_MODEL.BY_AMOUNT
                )
                if order:
                    try:
                        self.Broker.receive_order(QA_Event(order=order))
                        trade_mes = self.Broker.query_orders(
                            ac.account_cookie,
                            'filled'
                        )
                        # print(trade_mes)
                        res = trade_mes.loc[order.account_cookie,
                                            order.realorder_id]
                        order.trade(
                            res.trade_id,
                            res.trade_price,
                            res.trade_amount,
                            res.trade_time
                        )

                        # TODO: market_engine
                        self.write_message(
                            {
                                'topic':
                                'trade',
                                'status':
                                200,
                                'order_id':
                                order.realorder_id,
                                'mes':
                                'trade success TradeID: {} | Trade_Price: {} | Trade_Amount: {} | Trade_Time: | {}'
                                .format(
                                    res.trade_id,
                                    res.trade_price,
                                    res.trade_amount,
                                    res.trade_time
                                ),
                            }
                        )
                    except Exception as e:
                        self.write_message(
                            {
                                'topic': 'trade',
                                'status': 400,
                                'mes': str(e)
                            }
                        )
                else:
                    self.write_message(
                        {
                            'topic': 'trade',
                            'status': 500,
                            'mes': 'QATrader: Failed to create order'
                        }
                    )

        except Exception as e:
            print(e)

    def on_close(self):
        print('connection close')
