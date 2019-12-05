class Logger:
    def __init__(self, loggingLevel, topic=''):
        levels = ['debug', 'info', 'warning', 'critical', 'error']
        if isinstance(loggingLevel, int):
            self.loggingLevel = loggingLevel
        elif isinstance(loggingLevel, str):
            self.loggingLevel = levels.index(loggingLevel)
        self.topic = topic

    def getMsg(self, objects):
        msg = ''
        for x in range(len(objects)):
            msg += ' ' + objects[x]
        return msg

    def debug(self, *objects):
        msg = self.getMsg(objects)
        if self.loggingLevel <= 0:
            print('[DEBUG]    ', self.topic, msg)

    def info(self, *objects):
        msg = self.getMsg(objects)
        if self.loggingLevel <= 1:
            print('[INFO]     ', self.topic, msg)

    def warning(self, *objects):
        msg = self.getMsg(objects)
        if self.loggingLevel <= 2:
            print('[WARNING]  ', self.topic, msg)

    def critical(self, *objects):
        msg = self.getMsg(objects)
        if self.loggingLevel <= 3:
            print('[CRITICAL] ', self.topic, msg)

    def error(self, *objects):
        msg = self.getMsg(objects)
        if self.loggingLevel <= 4:
            print('[ERROR]    ', self.topic, msg)
