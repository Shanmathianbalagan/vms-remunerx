from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.security import create_access_token
from app.services.auth_service import authenticate_against_payroll_view, sync_local_identity

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    view_row = authenticate_against_payroll_view(db, payload.email, payload.password)

    if view_row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user = sync_local_identity(db, view_row)

    token = create_access_token({"sub": str(user.user_id), "role": user.role})

    return LoginResponse(
        access_token=token,
        user_id=user.user_id,
        employee_id=user.employee_id,
        name=view_row["username"],
        email=user.email,
        role=user.role,
    )
