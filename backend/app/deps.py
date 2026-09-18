from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.security import decode_access_token

bearer_scheme = HTTPBearer()


class CurrentUser:
    """Identity decoded straight from the JWT - no DB lookup needed. Credentials
    were already validated against vw_login_users at login time (see
    services/auth_service.py); this just carries what was issued in the token."""

    def __init__(self, payload: dict):
        self.sub: str = payload["sub"]
        self.role: str = payload.get("role", "EMPLOYEE")
        self.tenantid: int = payload.get("tenantid")
        self.empid: str | None = payload.get("empid")

    @property
    def is_admin(self) -> bool:
        return self.role == "ADMIN"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = decode_access_token(credentials.credentials)
    except JWTError:
        raise credentials_exception

    if payload.get("sub") is None:
        raise credentials_exception

    return CurrentUser(payload)


def get_current_empid(current_user: CurrentUser = Depends(get_current_user)) -> str:
    if not current_user.empid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is not linked to an employee record",
        )
    return current_user.empid


def get_current_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
