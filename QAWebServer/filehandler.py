import os
import uuid
import requests
from QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QASetting.QALocalize import cache_path
from QUANTAXIS.QAUtil.QAParameter import RUNNING_STATUS
from QUANTAXIS.QAUtil.QASetting import DATABASE


class FileHandler(QABaseHandler):

    def post(self):
        content = self.get_argument('content')
        title = self.get_argument('title', None)
        # if os.path.exists('{}{}{}.py'.format(cache_path, os.sep, title)):

        filename = str(uuid.uuid4())
        with open('{}{}{}.py'.format(cache_path, os.sep, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        res = {
            'filename': filename,
            'filepath': '{}{}{}.py'.format(cache_path, os.sep, filename),
            'content': content,
            'title': title
        }

        print(res)
        self.write({
            'result': res,
            'status': RUNNING_STATUS.SUCCESS
        })
        DATABASE.filename.insert_one(res)

    def get(self):
        filename = self.get_argument('filename', None)
        if filename is None:
            title = self.get_argument('title', None)
            if title:
                res = DATABASE.filename.find_one({'title': title})
                if res is not None:
                    filename = res['filename']
                    with open(res['filepath'], 'r', encoding='utf-8') as f:
                        r = f.read()

                    self.write({
                        'status': RUNNING_STATUS.SUCCESS,
                        'res': r
                    })
                else:
                    self.write({
                        'status': RUNNING_STATUS.WRONG,
                        'text': 'none title in database',
                        'res': {}
                    })
            else:
                self.write({
                    'status': RUNNING_STATUS.WRONG,
                    'text': 'none filename or title given',
                    'res': {}
                })
        else:
            with open('{}{}_{}.py'.format(cache_path, os.sep, filename), 'r', encoding='utf-8') as f:
                r = f.read()

            self.write({
                'status': RUNNING_STATUS.SUCCESS,
                'res': r
            })
