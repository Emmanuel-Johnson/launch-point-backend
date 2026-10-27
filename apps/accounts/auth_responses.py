from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


def set_refresh_token_cookie(response, refresh_token):
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_COOKIE_MAX_AGE,
        httponly=settings.REFRESH_TOKEN_COOKIE_HTTPONLY,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        path=settings.REFRESH_TOKEN_COOKIE_PATH,
    )


def clear_refresh_token_cookie(response):
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        path=settings.REFRESH_TOKEN_COOKIE_PATH,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
    )


def auth_response(result, status_code=200):
    """
    Return user information and the access token in JSON.
    Set the refresh token in an HttpOnly cookie.
    """
    result = result.copy()
    tokens = result.pop("tokens", None)

    if tokens:
        result["access"] = tokens["access"]

    response = Response(result, status=status_code)

    if tokens and tokens.get("refresh"):
        set_refresh_token_cookie(response, tokens["refresh"])

    return response


def logout_response(request):
    refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)

    if not refresh_token:
        response = Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )
        clear_refresh_token_cookie(response)
        return response

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

    except TokenError:
        # The token may already be expired or invalid.
        # The client should still be allowed to clear its session.
        pass

    response = Response(
        {"message": "Logout successful."},
        status=status.HTTP_200_OK,
    )

    clear_refresh_token_cookie(response)

    return response
