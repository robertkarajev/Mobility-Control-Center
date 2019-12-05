class Logger:
    def __init__(self, loggingLevel, topic=''):
        levels = ['debug', 'info', 'warning', 'critical', 'error']
        if isinstance(loggingLevel, int):
            self.loggingLevel = loggingLevel
        elif isinstance(loggingLevel, str):
            self.loggingLevel = levels.index(loggingLevel)
        self.topic = topic

    def debug(self, msg):
        if self.loggingLevel <= 0:
            print('[DEBUG]    ', self.topic, msg)

    def info(self, msg):
        if self.loggingLevel <= 1:
            print('[INFO]     ', self.topic, msg)

    def warning(self, msg):
        if self.loggingLevel <= 2:
            print('[WARNING]  ', self.topic, msg)

    def critical(self, msg):
        if self.loggingLevel <= 3:
            print('[CRITICAL] ', self.topic, msg)

    def error(self, msg):
        if self.loggingLevel <= 4:
            print('[ERROR]    ', self.topic, msg)
