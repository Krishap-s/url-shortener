class UserNotFoundException(Exception):
    def __str__(self):
        return "User Not Found"


class InvalidCredentials(Exception):
    def __str__(self):
        return "Invalid Credentials"
