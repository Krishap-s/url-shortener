class LinkNotFoundException(Exception):
    def __str__(self):
        return "Link Not Found"


class InvalidCredentials(Exception):
    def __str__(self):
        return "Invalid Credentials"
