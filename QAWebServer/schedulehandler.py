from datetime import datetime
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import RequestHandler, Application
from apscheduler.schedulers.tornado import TornadoScheduler
import threading
from QAWebServer.basehandles import QABaseHandler


"""
增加 mongodb 的数据读取






"""
scheduler = None
job_ids = []

# 初始化


def init_scheduler():
    global scheduler
    scheduler = TornadoScheduler()
    scheduler.start()
    print('[QAScheduler Init]APScheduler has been started')

# 要执行的定时任务在这里


def task1(options):
    print('{} [APScheduler][Task]-{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), options))
    print(threading.enumerate())


class MainHandler(QABaseHandler):
    def get(self):
        self.write(
            '<a href="/scheduler?job_id=1&action=add">add job</a><br><a href="/scheduler?job_id=1&action=remove">remove job</a>')


class QASchedulerHandler(QABaseHandler):
    def get(self):
        global job_ids
        job_id = self.get_query_argument('job_id', None)
        action = self.get_query_argument('action', None)
        if job_id:
            # add
            if 'add' == action:
                if job_id not in job_ids:
                    job_ids.append(job_id)
                    scheduler.add_job(task1, 'interval',
                                      seconds=3, id=job_id, args=(job_id,))
                    self.write('[TASK ADDED] - {}'.format(job_id))
                else:
                    self.write('[TASK EXISTS] - {}'.format(job_id))
            # remove
            elif 'remove' == action:
                if job_id in job_ids:
                    scheduler.remove_job(job_id)
                    job_ids.remove(job_id)
                    self.write('[TASK REMOVED] - {}'.format(job_id))
                else:
                    self.write('[TASK NOT FOUND] - {}'.format(job_id))
        else:
            self.write('[INVALID PARAMS] INVALID job_id or action')


# if __name__ == "__main__":
#     routes = [
#         # (r"/", QAMainHandler),
#         (r"/scheduler/?", QASchedulerHandler),
#     ]
#     init_scheduler()
#     app = Application(routes, debug=True)
#     app.listen(8888)
#     IOLoop.current().start()
