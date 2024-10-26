class ValidationException(Exception):
    def __init__(self, message="Ocorreu um erro"):
        self.message = message
        super().__init__(self.message)

class ServiceUserException(Exception):
    def __init__(self, message="Ocorreu um erro"):
        self.message = message
        super().__init__(self.message)
