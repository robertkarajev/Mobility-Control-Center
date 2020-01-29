class Logger:
    # there are different loggingLevels. 0=debug,1=info,2=warning,3=critical,4=error
    # when making a logger it will log things that are of that importance and higher
    # 0 will log everything while 4 will only log errors
    # you can give logs a topic which they will print
    # when giving the logger a topic it will only print logs of that topic
    # if you don't give the logger a topic it'll print all the logs (if the loggingLevel allows it)
    # copyright free :)
    def __init__(self, loggingLevel, topic=''):
        levels = ['debug', 'info', 'warning', 'critical', 'error']
        if isinstance(loggingLevel, int):
            self.loggingLevel = loggingLevel
        elif isinstance(loggingLevel, str):
            self.loggingLevel = levels.index(loggingLevel.lower())
        self.topic = topic

    # a function which makes it possible to print everything
    def print(self, *objects):
        if objects[1]:
            objects = objects[:2] + (':',) + objects[2:]
        if self.topic == '':
            print(*objects)
        elif self.topic == objects[1]:
            print(*objects)

    # methods which indicate of what importance the log is
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
