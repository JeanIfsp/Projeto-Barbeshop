class ValidationException(Exception):
    def __init__(self, message="Ocorreu um erro"):
        self.message = message
        super().__init__(self.message)

class ServiceClientException(Exception):
    def __init__(self, message="Ocorreu um erro"):
        self.message = message
        super().__init__(self.message)
