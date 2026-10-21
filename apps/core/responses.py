from typing import Any

from rest_framework import status
from rest_framework.response import Response


def success_response(
    message: str,
    data: Any = None,
    meta: dict[str, Any] | None = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
            "errors": None,
            "meta": meta,
        },
        status=status_code,
    )


def error_response(
    message: str,
    errors: Any = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors,
            "meta": None,
        },
        status=status_code,
    )
