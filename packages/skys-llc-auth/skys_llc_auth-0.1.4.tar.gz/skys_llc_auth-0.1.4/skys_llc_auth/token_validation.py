from dataclasses import dataclass

import jwt
from fastapi import Request, status
from pydantic_settings import BaseSettings

from skys_llc_auth.exceptions import ParamsError, TokenError
from skys_llc_auth.utils import Singleton, TokenType, UserRole


class DefaultTokenParams(Singleton):
    def __init__(
        self,
        key: str | None = None,
        algorithms: str | None = None,
        *,
        config: BaseSettings | None = None,
    ) -> None:
        if key is not None and algorithms is not None:
            self.key = key
            self.algorithms = algorithms
        elif issubclass(config.__class__, BaseSettings):
            if hasattr(config, "public_key"):
                self.key = config.public_key  # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
            if hasattr(config, "ALGORITHMS"):
                self.algorithms = config.ALGORITHMS  # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
        else:
            raise ParamsError("key and algorithms, or config class must be provided")


@dataclass(slots=True)
class TokenValidation:
    token: str
    deftokenpar: DefaultTokenParams
    role: UserRole | list[UserRole] | None = None
    token_user_id: str | None = None
    token_type_jwt: str | None = None
    token_user_role: str | None = None
    token_is_access: bool | None = None
    token_is_refresh: bool | None = None

    def __post_init__(self):
        if self.deftokenpar.key is None:
            raise ParamsError("key is not provided")
        if self.deftokenpar.algorithms is None:
            raise ParamsError("algorithm is not provided")

    def _decode(self) -> dict[str, str]:
        try:
            token = jwt.decode(
                self.token,
                key=self.deftokenpar.key,
                algorithms=[self.deftokenpar.algorithms],
            )
            return dict(token)
        except jwt.PyJWTError as exp_err:
            raise TokenError(
                detail=str(exp_err.args),
                status_code=status.HTTP_401_UNAUTHORIZED,
            ) from exp_err

    def _has_access(self) -> bool:
        if isinstance(self.role, list):
            return self._decode().get("role", None) in [i.value for i in self.role]
        elif isinstance(self.role, UserRole):
            return self._decode().get("role", None) == self.role.value
        else:
            raise ParamsError("expected type role is list[UserRole] or UserRole")

    def _not_access(self) -> bool:
        if isinstance(self.role, list):
            return self._decode().get("role", None) not in [i.value for i in self.role]
        elif isinstance(self.role, UserRole):
            return self._decode().get("role", None) != self.role.value
        else:
            raise ParamsError("expected type role is list[UserRole] or UserRole")

    def check_permission(self, role: list[UserRole] | UserRole | None = None, *, exclude: bool) -> None:
        if self.role is None and role is None:
            raise ParamsError("role is not provided")
        self.role = role
        access_token = self._not_access() if exclude else self._has_access()
        if not access_token:
            raise TokenError(
                detail="Permission denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )

    def user_id(self) -> str:
        if self.token_user_id is not None:
            return self.token_user_id
        user_id = self._decode().get("id", None)
        if user_id:
            self.token_user_id = user_id
            return user_id
        raise TokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token must have key id",
        )

    def user_role(self) -> str | None:
        if self.token_user_role is not None:
            return self.token_user_role
        user_role = self._decode().get("role", None)
        if user_role:
            self.token_user_role = user_role
            return user_role
        raise TokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token must have key role",
        )

    def _token_type_jwt(self) -> str | None:
        if self.token_type_jwt is not None:
            return self.token_type_jwt
        token_type = self._decode().get("token_type_jwt", None)
        if token_type:
            self.token_type_jwt = token_type
            return token_type
        raise TokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token must have key type_jwt",
        )

    def is_access(self) -> bool:
        if self.token_is_access is not None:
            return self.token_is_access
        self.token_is_access = self._token_type_jwt() == TokenType.access.value
        return self.token_is_access

    def is_refresh(self) -> bool:
        if self.token_is_refresh is not None:
            return self.token_is_refresh
        self.token_is_refresh = self._token_type_jwt() == TokenType.refresh.value
        return self.token_is_refresh


async def get_token_from_request(request: Request) -> str:  # pragma: no cover
    if not request.headers.get("Authorization", None):
        raise TokenError(
            detail="Request must have a Authorization token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = request.headers["Authorization"].split(" ")
    if token[0] != "Bearer":
        raise TokenError(
            detail="Предоставлен не Bearer токен",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if len(token) != 2:
        raise TokenError(
            detail="Invalid basic header. Credentials string should not contain spaces.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return token[1]
