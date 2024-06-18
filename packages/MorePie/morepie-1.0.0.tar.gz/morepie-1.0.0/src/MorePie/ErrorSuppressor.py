class ErrorSuppressor:
    def __init__(self, errors: tuple[Exception] = ()):
        self.err = errors

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.err:
            return True
        if exc_type in self.err:
            return True
        return False

def CreateErrorSuppressor(*errors: Exception | BaseException | type) -> ErrorSuppressor:
    return ErrorSuppressor(tuple(errors))