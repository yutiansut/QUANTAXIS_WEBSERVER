from QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QAUtil.QASetting import DATABASE


class QAPositionHandler(QABaseHandler):
    def get(self):
        """get spms's

        Arguments:
            self {[type]} -- [description]
        """
        action = self.get_argument('action')
        portfolio = self.get_argument('portfolio')
        res = [item for item in DATABASE.positions.find(
            {'portfolio_cookie': portfolio}, {'_id': 0})]
        print(res)
        self.write({'result': res})
