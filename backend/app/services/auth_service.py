from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.user import User
from app.security import verify_password


def authenticate_against_payroll_view(db: Session, email: str, password: str) -> dict | None:
    """
    Validates credentials against vw_login_users (the payroll system's combined
    admin + employee login view). Admin-type rows (usertype='SECURITYADMIN')
    are checked against their bcrypt password_hash; employee-type rows
    (usertype='INDIVIDUAL') don't have a hash yet, so they're checked as
    plain text for now, per the payroll team's current setup.
    """
    row = db.execute(
        text("SELECT * FROM vw_login_users WHERE email = :email"), {"email": email}
    ).mappings().first()

    if row is None:
        return None

    if row["password_hash"]:
        if not verify_password(password, row["password_hash"]):
            return None
    else:
        if password != row["password"]:
            return None

    return dict(row)


def sync_local_identity(db: Session, view_row: dict) -> User:
    """
    Our own Visit/Approval/etc. tables still key off our own small integer
    employee_id, not the payroll system's empid/userid. This keeps that
    working by mirroring the authenticated payroll identity into our local
    employees/users tables (creating them on first login), rather than
    rewriting every table that references employee_id.
    """
    email = view_row["email"]
    role = view_row["role"]

    employee = db.query(Employee).filter(Employee.email == email).first()
    if employee is None:
        employee = Employee(
            name=view_row["username"],
            email=email,
            tenant_id=view_row["tenantid"],
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        user = User(
            email=email,
            password_hash="",  # credentials are validated against vw_login_users, not this row
            role=role,
            employee_id=employee.employee_id,
            tenant_id=view_row["tenantid"],
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.role != role:
        user.role = role
        db.commit()
        db.refresh(user)

    return user
