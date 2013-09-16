class WindowNotFound:
    def __init__(self, info):
        self.info = info
    def __str__(self):
        return self.info.encode('gb2312', errors = 'ignore')
