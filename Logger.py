from datetime import datetime

class Logger:
    _instance = None
    def set_fmt(self, fmt):
        self.fmt = fmt

    def set_date_fmt(self, d_fmt):
        self.d_fmt = d_fmt

    def set_out(self, f):
        if f == None:
            self.out = None
        else:
            self.out = f

    def Log(self, msg):
        MSG = msg
        DATE = datetime.now().strftime(self.d_fmt)
        log_msg = self.fmt.format(MSG=MSG, DATE=DATE)
        if self.out == None:
            print(log_msg)
        else:
            Logger.fileLog(self.out, log_msg+'\n')
    
    @classmethod
    def getLogger(cls):
        if cls._instance == None:
            cls._instance = Logger()
            return cls._instance

    @staticmethod
    def fileLog(f, msg):
        with open(f, 'a+') as file:
            file.write(msg)
            

logger = Logger.getLogger()
logger.set_date_fmt("%H:%M:%S")
logger.set_out('log.app');
logger.set_fmt("{DATE} -> {MSG}")

logger.Log("something happen")
