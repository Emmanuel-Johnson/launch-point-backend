from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from apps.core.responses import error_response


def custom_exception_handler(exc, context) -> Response | None:
    # Let DRF handle standard API exceptions first.
    response = drf_exception_handler(exc, context)

    # Unexpected exceptions are handled by Django as HTTP 500 errors.
    if response is None:
        return None

    # Handle serializer validation errors.
    if isinstance(exc, exceptions.ValidationError):
        message = "Validation failed."
        errors = response.data

    # Handle standard API errors, such as 404, 401, and 403.
    else:
        detail = response.data.get("detail")

        if detail is not None:
            message = str(detail)
            errors = None
        else:
            message = "Request failed."
            errors = response.data

    # Return every handled API error in the standard envelope.
    return error_response(
        message=message,
        errors=errors,
        status_code=response.status_code,
    )
