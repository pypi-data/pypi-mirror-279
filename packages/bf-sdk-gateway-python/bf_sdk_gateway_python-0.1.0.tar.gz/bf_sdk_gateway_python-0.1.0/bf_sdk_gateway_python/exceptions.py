class BemFacilPaymentError(Exception):
    """Base class for other exceptions"""
    pass


class InvalidTransactionError(BemFacilPaymentError):
    """Raised when a transaction is invalid"""
    pass


class AuthorizationError(BemFacilPaymentError):
    """Raised when there is an authorization error"""
    pass
