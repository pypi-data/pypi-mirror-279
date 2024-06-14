class PyAssemblyPaymentsException(Exception):
    pass


class PyAssemblyPaymentsNotImplementedException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsBadRequestException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsUnauthorisedException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsForbiddenException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsNotFoundException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsConflictException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsUnprocessableEntityException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsInternalErrorException(PyAssemblyPaymentsException):
    pass


class PyAssemblyPaymentsInsufficientFundsException(PyAssemblyPaymentsException):
    pass


def handle422(response_text):
    """Parse 422 error message to return correct exception."""
    if (
        "The account you're transacting from does not have enough funds available"
        in response_text
    ):
        raise PyAssemblyPaymentsInsufficientFundsException(response_text)
    raise PyAssemblyPaymentsUnprocessableEntityException(response_text)
