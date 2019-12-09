class Logger:
    def __init__(self, loggingLevel, topic=''):
        levels = ['debug', 'info', 'warning', 'critical', 'error']
        if isinstance(loggingLevel, int):
            self.loggingLevel = loggingLevel
        elif isinstance(loggingLevel, str):
            self.loggingLevel = levels.index(loggingLevel.lower())
        self.topic = topic

    def print(self, *objects):
        if objects[1]:
            objects = objects[:2] + (':',) + objects[2:]
        if self.topic == '':
            print(*objects)
        elif self.topic == objects[1]:
            print(*objects)

    def debug(self, *objects, topic=''):
        if self.loggingLevel <= 0:
            self.print('[DEBUG]   ', topic, *objects)

    def info(self, *objects, topic=''):
        if self.loggingLevel <= 1:
            self.print('[INFO]    ', topic, *objects)

    def warning(self, *objects, topic=''):
        if self.loggingLevel <= 2:
            self.print('[WARNING] ', topic, *objects)

    def critical(self, *objects, topic=''):
        if self.loggingLevel <= 3:
            self.print('[CRITICAL]', topic, *objects)

    def error(self, *objects, topic=''):
        if self.loggingLevel <= 4:
            self.print('[ERROR]   ', topic, *objects)
