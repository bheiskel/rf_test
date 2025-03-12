class RFTestException(Exception):
    def __init__(self, *args):
        if args:
            self.message = f'{" - ".join(map(str,args))}'
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'RFTestException, {}'.format(self.message)
        else:
            return 'RFTestException occurred'
