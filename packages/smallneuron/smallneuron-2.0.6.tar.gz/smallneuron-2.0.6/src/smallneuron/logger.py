import syslog
from datetime import datetime
from time import time
import sys

class Logger:
    perf_enable=False
    prev_time=time()
    logLevel=syslog.LOG_DEBUG
    def __init__(self, service_name):
        self.service_name = service_name
        self.prefix=""

    def error(self, *args):
        if syslog.LOG_ERR <= Logger.logLevel:
            self.__logger(syslog.LOG_ERR, *args)

    def warn(self, *args):
        if syslog.LOG_WARNING <= Logger.logLevel:
            self.__logger(syslog.LOG_WARNING, *args)

    def notice(self, *args):
        if syslog.LOG_NOTICE <= Logger.logLevel:
            self.__logger(syslog.LOG_NOTICE, *args)

    def info(self, *args):
        if syslog.LOG_INFO <= Logger.logLevel:
            self.__logger(syslog.LOG_INFO, *args)

    def debug(self, *args):
        if syslog.LOG_DEBUG <= Logger.logLevel:
            self.__logger(syslog.LOG_DEBUG, *args)

    def set_level(level):
        Logger.logLevel=level

    def set_perf(setOn):
        Logger.perf_enable=setOn

    def perfMark(self,text):
        if Logger.perf_enable:
            t=time()
            print(self.service_name, t, t-Logger.prev_time, text, file=sys.stderr)
            Logger.prev_time=t
        
    def __logger(self, severity, *args):
        try:
            syslog.openlog(self.service_name, syslog.LOG_CONS | syslog.LOG_PID | syslog.LOG_NDELAY, syslog.LOG_LOCAL1)
            msg = ""
            for a in args:
                msg = msg + " " + str(a)

            syslog.syslog(severity, msg)
            syslog.closelog()
        except Exception as e:
            print("Syslog fail ", e)

    def ___current_full_date(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    


