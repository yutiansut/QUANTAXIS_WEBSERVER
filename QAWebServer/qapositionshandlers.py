from QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QAUtil.QASetting import DATABASE


class QAPositionHandler(QABaseHandler):
    def get(self):
        """get spms's

        Arguments:
            self {[type]} -- [description]
        """
        action = self.get_argument('action', 'query_portfolio')
        if action == 'query_portfolio':
        portfolio = self.get_argument('portfolio')
         user = self.get_argument('user')
          res = []
           for item in DATABASE.positions.find({'portfolio_cookie': portfolio, 'user_cookie': user}, {'_id': 0}):

                tres = dict(zip(item.keys(),
                                ["%.2f" % x if isinstance(x, float) else x for x in item.values()]))
                res.append(tres)
            self.write({'result': res})

        elif action == 'query_singlepos':
            portfolio = self.get_argument('portfolio')
            user = self.get_argument('user')
            pms_id = self.get_argument('pms_id')
            pos = DATABASE.positions.find_one(
                {'portfolio_cookie': portfolio, 'user_cookie': user, 'position_id': pms_id}, {'_id': 0})
            pos =dict(zip(pos.keys(),
                                ["%.2f" % x if isinstance(x, float) else x for x in pos.values()]))
            self.write({'result': pos})
