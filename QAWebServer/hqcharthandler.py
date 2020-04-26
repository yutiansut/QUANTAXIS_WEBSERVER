# #[derive(Deserialize, Clone, Serialize, Debug)]
# pub struct HqTrendSlice {
#     pub price: f64,
#     pub open: f64,
#     pub high: f64,
#     pub low: f64,
#     pub vol: f64,
#     pub amount: f64,
#     pub time: String,
#     pub avprice: f64,
#     pub increase: f64,
#     pub risefall: f64,
#     pub code: String,
#     pub close: f64,
# }

# #[derive(Deserialize, Clone, Serialize, Debug)]
# pub struct HqTrend {
#     pub name: String,
#     pub symbol: String,
#     pub time: String,
#     pub date: String,
#     pub price: f64,
#     pub open: f64,
#     pub yclose: f64,
#     pub high: f64,
#     pub low: f64,
#     pub vol: f64,
#     pub amount: f64,
#     pub minutecount: f64,
#     pub minute: Vec<HqTrendSlice>,
# }


"""
a python api for hqchart api
"""
from QAWebServer.basehandles import QABaseHandler
import QUANTAXIS as QA
import pandas as pd
import datetime

stocklist =  QA.QA_fetch_stock_list_adv()
class HqTrendSlice():
    def __init__(self):
        self.price = 0
        self.open = 0
        self.high = 0
        self.low = 0
        self.vol = 0
        self.amount = 0
        self.time = 0
        self.code = ''
        self.close = 0

    @property
    def avgprice(self):
        return 0

    @property
    def increase(self):
        return 0

    @property
    def risefall(self):
        return 0

    def to_json(self):
        return {
            'price': self.price,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'vol': self.vol,
            'amount': self.amount,
            'time': self.time,
            'avgprice': self.avgprice,
            'increase': self.increase,
            'risefall': self.risefall,
            'code': self.code,
            'close': self.close

        }


class HqTrend():
    def __init__(self, ):
        self.symbol = '000001'
        self.time = ''
        self.date = ''
        self.price = ''
        self.open = ''
        self.yclose = ''

        self.amount = 0
        self.vol = 0
        self.low = 0
        self.high = 0
        self.minutecount = 0
        self.minute = []

    def recv(self):
        self.minute.append(HqTrendSlice().to_json())

    def to_json(self):
        return {
            'name': stocklist.loc[self.symbol[0:6]]['name'],
            'symbol': self.symbol,
            'time': self.time,
            'date': self.date,
            'price': self.price,
            'open': self.open,
            'yclose': self.yclose,
            'amount': self.amount,
            'vol': self.vol,
            'low': self.low,
            'high': self.high,
            'minutecount': self.minutecount,
            'minute': self.minute}


class HqKline():
    def __init__(self, code, start, end, frequence, market):
        self.symbol = code

        self.start = start
        self.end = end
        self.frequence = frequence
        self.market = market

    @property
    def name(self):
      try:
          if self.market == 'stock_cn':
            return stocklist.loc[self.symbol[0:6]]['name']
          else:
            return self.symbol
      except:
          return ''


    @property
    def data(self):

        data = QA.QA_quotation(self.symbol, self.start, self.end, self.frequence, self.market, source=QA.DATASOURCE.MONGO, output=QA.OUTPUT_FORMAT.DATASTRUCT).data.reset_index()
        print(data)
        if self.frequence != 'day':
            data = data.assign(date= data.datetime.apply(lambda x: str(x)[0:10]))
        if self.market != 'stock_cn': 
            data =  data.assign(amount = data.volume * data.close)
        return data
        # return QA.QA_fetch_stock_day(self.symbol[0:6], self.start, self.end, 'pd')

    def klineformat(self):
        return []

    def to_json(self):

        return {
            "data": self.data.assign(date=self.data.date.apply(lambda x: QA.QA_util_date_str2int(str(x)[0:10])), yclose=self.data.close.shift().bfill()).loc[:, ['date', 'yclose', 'open', 'high', 'low', 'close', 'volume', 'amount']].values.tolist(),
            "symbol": self.symbol,  # 股票代码
            "name": self.name,  # 股票名称
            "start": 4837,  # 返回数据的起始位置 （暂时不用， 分页下载历史数据使用，下载都是一次请求完)
            "end": 3838,  # 返回数据的结束位置（暂时不用， 分页下载历史数据使用，下载都是一次请求完)
            "count": 4838,  # 需要的K线数据个数 ， 单位是天
            "ticket": 0,
            "version": "2.0",
            "message": '',
            "code": 0,
            "servertime": str(datetime.datetime.now())}


class QAHqchartDailyHandler(QABaseHandler):
    def get(self):

        t = HqTrend()
        t.recv()
        self.write({'result': t.to_json()})


class QAHqchartKlineHandler(QABaseHandler):
    def get(self):
        code = self.get_argument('code', '600000.sh')
        start = self.get_argument('start', '2019-01-01')
        end = self.get_argument('end', default='2020-01-01')
        frequence = self.get_argument('frequence', 'day')
        market = self.get_argument('market', 'stock_cn')

        t = HqKline(code, start, end, frequence, market)
        # t#.recv()
        self.write({'result': t.to_json()})


if __name__ == "__main__":
    import tornado
    from tornado.web import Application, RequestHandler, authenticated
    from tornado.websocket import WebSocketHandler

    app = Application(
        handlers=[
            (r"/test",  QAHqchartDailyHandler),
            (r"/testk", QAHqchartKlineHandler)
        ],
        debug=True
    )
    app.listen(8029)
    tornado.ioloop.IOLoop.current().start()
