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
        self.name = ''
        self.symbol = ''
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
            'name': self.name,
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


class QAHqchartHandler(QABaseHandler):
    def get(self):

        t = HqTrend()
        t.recv()
        self.write({'result': t.to_json()})


if __name__ == "__main__":
    import tornado
    from tornado.web import Application, RequestHandler, authenticated
    from tornado.websocket import WebSocketHandler

    app = Application(
        handlers=[
            (r"/test",  QAHqchartHandler),
        ],
        debug=True
    )
    app.listen(8029)
    tornado.ioloop.IOLoop.current().start()
