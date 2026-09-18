from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.security import create_access_token
from app.services.auth_service import authenticate_against_payroll_view

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    row = authenticate_against_payroll_view(db, payload.email, payload.password)

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    is_admin = row["usertype"] == "SECURITYADMIN"
    empid = None if is_admin else row["userid"]

    token = create_access_token(
        {
            "sub": str(row["userid"]),
            "role": row["role"],
            "tenantid": row["tenantid"],
            "empid": empid,
        }
    )

    return LoginResponse(
        access_token=token,
        user_id=str(row["userid"]),
        empid=empid,
        tenantid=row["tenantid"],
        name=row["username"],
        email=row["email"],
        role=row["role"],
    )
