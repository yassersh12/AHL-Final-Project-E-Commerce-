
class InvalidPasswordException(Exception):
    def __init__(self, message="Password does not meet security requirements."):
        self.message = message
        super().__init__(self.message)