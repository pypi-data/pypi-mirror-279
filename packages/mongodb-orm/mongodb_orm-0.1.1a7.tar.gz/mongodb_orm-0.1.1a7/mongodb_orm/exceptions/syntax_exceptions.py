class ChainingError(Exception):
    def __init__(self, message):
        self.context = {'status': 500}
        super().__init__(message)
