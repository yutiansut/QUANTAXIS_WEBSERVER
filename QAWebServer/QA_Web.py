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
import asyncio
import os
import sys

import tornado
#from terminado import SingleTermManager, TermSocket
from tornado.options import (define, options, parse_command_line,
                             parse_config_file)
from tornado.web import Application, RequestHandler, authenticated
from tornado_http2.server import Server

from QAWebServer.arphandles import (AccountHandler, PortfolioHandler,
                                    RiskHandler)
from QAWebServer.basehandles import QABaseHandler
from QAWebServer.commandhandler import (CommandHandler, CommandHandlerWS,
                                        RunnerHandler)
from QAWebServer.datahandles import (DataFetcher, StockBlockHandler, CurrentListHandler,
                                     StockCodeHandler, StockdayHandler,
                                     StockminHandler, StockPriceHandler,
                                     FutureCodeHandler)
from QAWebServer.filehandler import FileHandler
from QAWebServer.jobhandler import FileRunHandler, JOBHandler
from QAWebServer.quotationhandles import (MonitorSocketHandler,
                                          RealtimeSocketHandler,
                                          SimulateSocketHandler,
                                          future_realtime, stock_realtime, price_realtime)
from QAWebServer.strategyhandlers import BacktestHandler, StrategyHandler
from QAWebServer.tradehandles import AccModelHandler, TradeInfoHandler
from QAWebServer.userhandles import (PersonBlockHandler, SigninHandler,
                                     SignupHandler, UserHandler)
from QUANTAXIS import __version__
from QUANTAXIS.QAUtil.QASetting import QASETTING


class INDEX(QABaseHandler):

    def get(self):
        self.write(
            {
                'status': 200,
                'message': 'This is a welcome page for quantaxis backend',
                'github_page':
                'https://github.com/yutiansut/QUANTAXIS_WEBSERVER/blob/master/backendapi.md',
                'url': [item[0] for item in handlers]
            }
        )


#term_manager = SingleTermManager(shell_command=['bash'])
handlers = [
    (r"/",
     INDEX),
    (r"/codelist",
     CurrentListHandler),
    (r"/marketdata/future/code",
     FutureCodeHandler),
    (r"/marketdata/stock/day",
     StockdayHandler),
    (r"/marketdata/stock/min",
     StockminHandler),
    (r"/marketdata/fetcher",
     DataFetcher),
    (r"/marketdata/stock/block",
     StockBlockHandler),
    (r"/marketdata/stock/price",
     StockPriceHandler),
    (r"/marketdata/stock/code",
     StockCodeHandler),
    (r"/user/signin",
     SigninHandler),
    (r"/user/signup",
     SignupHandler),
    (r"/user",
     UserHandler),
    (r"/portfolio",
     PortfolioHandler),
    (r"/account",
     AccountHandler),
    (r"/user/blocksetting",
     PersonBlockHandler),
    (r"/strategy/content",
     StrategyHandler),
    (r"/backtest/content",
     BacktestHandler),
    (r"/trade",
     AccModelHandler),
    (r"/tradeinfo",
     TradeInfoHandler),
    (r"/realtime",
     RealtimeSocketHandler),
    (r"/realtime/stock",
     stock_realtime),
    (r"/realtime/future",
     future_realtime),
    (r"/realtime/price",
     price_realtime),
    (r"/simulate",
     SimulateSocketHandler),
    (r"/monitor",
     MonitorSocketHandler),
    (r"/risk",
     RiskHandler),
    (r"/command/run",
     CommandHandler),
    (r"/command/runws",
     CommandHandlerWS),
    (r"/command/runbacktest",
     RunnerHandler),
    (r"/command/jobmapper",
     JOBHandler),
    (r"/command/filemapper",
     FileRunHandler),
    (r"/file",
     FileHandler)
]


def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    define("port", default=8010, type=int, help="服务器监听端口号")

    define("address", default='0.0.0.0', type=str, help='服务器地址')
    define("content", default=[], type=str, multiple=True, help="控制台输出内容")

    parse_command_line()
    port = options.port
    address = options.address

    start_server(handlers, address, port)


def start_server(handlers, address, port):
    apps = Application(
        handlers=handlers,
        debug=True,
        autoreload=True,
        compress_response=True
    )
    http_server = Server(apps)
    print('========WELCOME QUANTAXIS_WEBSERVER============')
    print('QUANTAXIS VERSION: {}'.format(__version__))
    print('QUANTAXIS WEBSERVER is Listening on: http://localhost:{}'.format(port))
    print('请打开浏览器/使用JavaScript等来使用该后台, 并且不要关闭当前命令行窗口')
    http_server.bind(port=port, address=address)
    """增加了对于非windows下的机器多进程的支持
    """
    http_server.start(1)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
