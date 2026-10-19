"""Service layer: exceptions that express the alternative flows of the use case specifications."""


class ServiceError(Exception):
    """Base class; the controller turns it into a readable message for the user."""


class NotFound(ServiceError):
    pass


class PermissionDenied(ServiceError):
    pass


class ValidationError(ServiceError):
    pass


class CheckoutError(ServiceError):

    def __init__(self, problems):
        super().__init__("; ".join(problems))
        self.problems = problems
