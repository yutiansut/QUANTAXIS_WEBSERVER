# encoding=utf-8
import inspect
import logging
import os
import sys

import servicemanager
import win32event
import win32service
import win32serviceutil
import winerror

from QAWebServer.QA_Web import main
from QUANTAXIS.QASetting.QALocalize import log_path


class QUANTAXIS_WebService(win32serviceutil.ServiceFramework):

    _svc_name_ = "QUANTAXIS_WebService"  # 服务名
    _svc_display_name_ = "QUANTAXIS"  # 服务在windows系统中显示的名称
    _svc_description_ = "QUANTAXIS 后台服务 "  # 服务的描述

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.run = True

    def _getLogger(self):

        logger = logging.getLogger('[QUANTAXIS_WebService]')

        #this_file = inspect.getfile(inspect.currentframe())
        # dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler('{}{}{}'.format(
            log_path, os.sep, "QUANTAXIS_WebService.log"))

        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):

        self.logger.info("QUANTAXIS WEBSERVICE START")
        while self.run:
            main()

    def SvcStop(self):
        self.logger.info("QUANTAXIS WEB SERVICE is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


def servicemain():
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(QUANTAXIS_WebService)
            servicemanager.Initialize('QUANTAXIS_WebService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(QUANTAXIS_WebService)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(QUANTAXIS_WebService)
            servicemanager.Initialize('QUANTAXIS_WebService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(QUANTAXIS_WebService)
