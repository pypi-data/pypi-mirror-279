from __future__ import annotations

import re
from collections.abc import Iterable

from drakaina.constants import ENV_AUTH_EXCEPTION
from drakaina.constants import ENV_AUTH_PAYLOAD
from drakaina.constants import ENV_AUTH_SCOPES
from drakaina.constants import ENV_IS_AUTHENTICATED
from drakaina.constants import ENV_USER
from drakaina.constants import ENV_USER_ID
from drakaina.contrib.jwt import SUPPORTED_ALGORITHMS
from drakaina.contrib.jwt.errors import InvalidJWTTokenError
from drakaina.contrib.jwt.types import RevokeChecker
from drakaina.contrib.jwt.types import ScopesGetter
from drakaina.contrib.jwt.types import TokenGetter
from drakaina.contrib.jwt.types import UserGetter
from drakaina.contrib.jwt.utils import decode_jwt_token
from drakaina.exceptions import AuthenticationFailedError
from drakaina.exceptions import ForbiddenError
from drakaina.middleware.base import BaseMiddleware
from drakaina.types import ASGIReceive
from drakaina.types import ASGIScope
from drakaina.types import ASGISend
from drakaina.types import WSGIApplication
from drakaina.types import WSGIEnvironment
from drakaina.types import WSGIResponse
from drakaina.types import WSGIStartResponse
from drakaina.utils import get_cookies
from drakaina.utils import iterable_str_arg


class JWTAuthenticationMiddleware(BaseMiddleware):
    """The middleware supporting JWT tokens.

    :param app: WSGI Application.
    :param algorithms: List of supported algorithms.
    :param secret_key: A secret key for signature verification.
    :param public_key: Public key for signature verification in
        asymmetric algorithms.
    :param credentials_required: If `True`, the request is expected to
        contain credential data. If they are missing, an exception is raised.
        Default: `True`.
    :param prefix: The token prefix in the authorization headers.
        Default: `"Bearer"`.
    :param use_cookies: If true, the token will be searched in the cookie
        headers for the specified key. Default: `False`.
    :param cookie_key: The key by which the token is stored in the cookie
        headers.
    :param decode_options: The dictionary is passed as is as the `options`
        argument to the `pyjwt.decode` function. Default: `{
            "require": [],  # Require claims
            "verify_iss": False,  # Issuer
            "verify_aud": False,  # Audience
            "verify_exp": True,   # Expiry
            "verify_nbf": False,  # Not Before
            "verify_iat": True,   # Issued at
            "verify_jti": False,  # JWT ID
        }`
    :param verify_values: A dictionary of key-value pairs, where key is
        the name of the key in the token payload, and the value to check can be
        a specific value, a list of possible values, or a re.Pattern object
        (the result of re.compile).
    :param leeway_value: The value of leeway in seconds. Default: `0`.
    :param user_id_field: The name of the key in the token payload to store
        the user ID. Default: `"user_id"`.
    :param token_getter: Callable for an alternative way to get a token.
    :param user_getter: Callable to retrieve a user object.
    :param scopes_getter: Callable to get permission scopes.
    :param revoke_checker: Callable to verify that the token is revoked.
    :param kwargs: Other arguments to pass to the constructor of the base class.

    """

    __slots__ = (
        "_algorithms",
        "__verify_key",
        "_credentials_required",
        "_prefix",
        "_cookie_key",
        "_decode_options",
        "_verify_values",
        "_leeway",
        "_user_id_field",
        "get_token",
        "get_user",
        "is_revoked",
        "get_scopes",
    )

    def __init__(
        self,
        app: WSGIApplication,
        algorithms: str | Iterable[str] = SUPPORTED_ALGORITHMS,
        secret_key: str = None,
        public_key: str = None,
        credentials_required: bool = True,
        prefix: str | Iterable[str] = "Bearer",
        use_cookies: bool = False,
        cookie_key: str = "jwt",
        decode_options: dict[str, bool | list[str]] | None = None,
        verify_values: (
            dict[str, str | Iterable[str] | re.Pattern] | None
        ) = None,
        leeway_value: int | float = 0,
        user_id_field: str = "user_id",
        token_getter: TokenGetter | None = None,
        user_getter: UserGetter | None = None,
        scopes_getter: ScopesGetter | None = None,
        revoke_checker: RevokeChecker | None = None,
        **kwargs,
    ):
        super().__init__(app, **kwargs)

        self._algorithms = iterable_str_arg(algorithms)
        self.__verify_key = secret_key or public_key
        self._credentials_required = credentials_required
        self._prefix = iterable_str_arg(prefix)
        self._cookie_key = cookie_key
        self._decode_options = (
            decode_options
            if decode_options is not None
            else {
                "require": [],
                "verify_iss": False,
                "verify_aud": False,
                "verify_exp": True,
                "verify_nbf": False,
                "verify_iat": True,
                "verify_jti": False,
            }
        )
        self._verify_values = verify_values if verify_values is not None else {}
        self._leeway = leeway_value
        self._user_id_field = user_id_field

        if callable(token_getter):
            self.get_token = token_getter
        elif use_cookies:
            self.get_token = self._token_from_cookies
        else:
            self.get_token = self._token_from_auth_header

        self.is_revoked = revoke_checker
        self.get_user = user_getter
        self.get_scopes = scopes_getter

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        if environ["REQUEST_METHOD"] == "OPTIONS":
            return self.app(environ, start_response)

        token = self.get_token(environ)

        if not token and self._credentials_required:
            raise AuthenticationFailedError("Credential required")

        if token is not None:
            try:
                token_payload = decode_jwt_token(
                    token=token,
                    algorithms=self._algorithms,
                    verify_key=self.__verify_key,
                    verify=True,
                    decode_options=self._decode_options,
                    verify_values=self._verify_values,
                    leeway=self._leeway,
                )
                token_is_valid = True
                token_exception = None
            except InvalidJWTTokenError as error:
                if self._credentials_required:
                    raise error
                else:
                    token_payload = decode_jwt_token(
                        token=token,
                        algorithms=self._algorithms,
                        verify_key=self.__verify_key,
                        verify=False,
                        decode_options=None,
                        verify_values=self._verify_values,
                        leeway=self._leeway,
                    )
                    token_is_valid = environ.get(ENV_IS_AUTHENTICATED, False)
                    token_exception = error

            if callable(self.is_revoked) and token_is_valid:
                if self.is_revoked(environ, token_payload):
                    raise ForbiddenError("Token is revoked")

            environ[ENV_AUTH_PAYLOAD] = token_payload
            environ[ENV_IS_AUTHENTICATED] = token_is_valid
            environ[ENV_AUTH_EXCEPTION] = token_exception
            environ[ENV_USER_ID] = token_payload.get(self._user_id_field)

            if callable(self.get_user) and token_is_valid:
                environ[ENV_USER] = self.get_user(environ, token_payload)
            if callable(self.get_scopes) and token_is_valid:
                environ[ENV_AUTH_SCOPES] = self.get_scopes(
                    environ,
                    token_payload,
                )

        return self.app(environ, start_response)

    async def __asgi_call__(
        self,
        scope: ASGIScope,
        receive: ASGIReceive,
        send: ASGISend,
    ):
        await self.app(scope, receive, send)

    def _token_from_auth_header(
        self,
        request: ASGIScope | WSGIEnvironment,
    ) -> str | None:
        auth_header = request.get("HTTP_AUTHORIZATION")
        if auth_header is None:
            return None

        try:
            parts = auth_header.strip().split(" ")
        except ValueError:
            raise AuthenticationFailedError("Invalid `Authorization` header")

        if len(parts) == 0 or parts[0] not in self._prefix:
            return None

        if len(parts) != 2:
            raise InvalidJWTTokenError(
                "The `Authorization` header must contain two values "
                "separated by a space",
            )

        return parts[1]

    def _token_from_cookies(
        self,
        request: ASGIScope | WSGIEnvironment,
    ) -> str | None:
        cookie_header = request.get("HTTP_COOKIE")
        if cookie_header is None:
            return None

        cookies = get_cookies(cookie_header)

        return cookies.get(self._cookie_key)
