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
import json

import tornado
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QAWebServer.basehandles import QABaseHandler, QAWebSocketHandler
from QAWebServer.util import CJsonEncoder
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_account, QA_fetch_risk
from QUANTAXIS.QASU.save_account import save_account
from QUANTAXIS.QASU.user import QA_user_sign_in, QA_user_sign_up
from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting


class MemberHandler(QABaseHandler):
    """
    获得所有的回测member
    """

    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 09:00:00 end-->now
        accounts?account_cookie=xxx
        """
        #account_cookie= self.get_argument('account_cookie', default='admin')

        query_account = QA_fetch_account()
        # data = [res for res in query_account]
        if len(query_account) > 0:
            #data = [QA.QA_Account().from_message(x) for x in query_account]
            def warpper(x):
                return str(x) if isinstance(x, datetime.datetime) else x

            res = []
            for item in query_account:
                res.append(
                    [
                        item['portfolio_cookie'],
                        item['account_cookie'],
                        str(item['start_date']),
                        str(item['end_date']),
                        'market_type'
                    ]
                )

            self.write({'result': res})
        else:
            self.write('WRONG')


class AccountHandler(QABaseHandler):
    """
    对于某个回测账户
    """

    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 09:00:00 end-->now
        accounts?account_cookie=xxx
        """
        account_cookie = self.get_argument('account_cookie', default='admin')

        query_account = QA_fetch_account({'account_cookie': account_cookie})
        #data = [QA_Account().from_message(x) for x in query_account]

        if len(query_account) > 0:
            #data = [QA.QA_Account().from_message(x) for x in query_account]
            def warpper(x):
                return str(x) if isinstance(x, datetime.datetime) else x

            for item in query_account:
                item['trade_index'] = list(map(str, item['trade_index']))
                item['history'] = [
                    list(map(warpper,
                             itemd)) for itemd in item['history']
                ]

            self.write({'result': query_account})
        else:
            self.write('WRONG')


class PortfolioHandler(QAWebSocketHandler):
    """[summary]

    Arguments:
        QABaseHandler {[type]} -- [description]

    /portfolio?

    params:
        action:
            - get_account
            - get_cash
            - get_history
        portfolio_cookie (必须项)
        user_cookie (必须项)


    """
    cache_dict = {}

    def get_portfolio(self, user_cookie, portfolio_cookie):
        """首先进行变量检查

        Arguments:
            user_cookie {[type]} -- [description]
            portfolio_cookie {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        if user_cookie is None or portfolio_cookie is None:
            return False
        else:
            try:
                portfolio = QA_Portfolio(
                    user_cookie=user_cookie,
                    portfolio_cookie=portfolio_cookie
                )
                return portfolio
            except:
                return False

    def get(self):
        action = self.get_argument('action', default='get_accounts')
        portfolio = self.get_portfolio(
            self.get_argument('user_cookie'),
            self.get_argument('portfolio_cookie')
        )
        print(portfolio)
        print(portfolio.accounts)
        if action == 'get_accounts':
            """获取该portfolio下的所有account
            """

            res = []
            for account in portfolio.accounts.values():

                res.append(account.message)
            self.write(
                {
                    'status': 200,
                    'result': res
                }
            )
        elif action == 'get_cash':
            """注意此处为portfolio的cash/ 不是account的
            """
            self.write({'status': 200, 'result': portfolio.cash_available})

    def post(self):
        action = self.get_argument('action', default='add_account')
        portfolio = self.get_portfolio(
            self.get_argument('user_cookie'),
            self.get_argument('portfolio_cookie')
        )

    def delete(self):
        action = self.get_argument('action', default='delete_account')
        portfolio = self.get_portfolio(
            self.get_argument('user_cookie'),
            self.get_argument('portfolio_cookie')
        )
        try:
            if portfolio.drop_account(self.get_argument('account_cookie')):
                self.write({'status': 200})
        except:
            self.write({'status': 404})
class RiskHandler(QABaseHandler):
    """
    回测账户的风险评价
    实时评估函数

    当我们给定一个 QA_Account/ QAPORTFOLIO中的


    """

    def get(self):



        
        account_cookie = self.get_argument('account_cookie', default='admin')

        query_account = QA_fetch_risk({'account_cookie': account_cookie})
        #data = [QA_Account().from_message(x) for x in query_account]
        if len(query_account) > 0:
            #data = [QA.QA_Account().from_message(x) for x in query_account]

            self.write({'result': query_account})
        else:
            self.write('WRONG')
