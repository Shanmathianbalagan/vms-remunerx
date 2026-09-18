from sqlalchemy import text
from sqlalchemy.orm import Session

from app.security import verify_password


def authenticate_against_payroll_view(db: Session, email: str, password: str) -> dict | None:
    """
    Validates credentials against vw_login_users (the payroll system's combined
    admin + employee login view). Admin-type rows (usertype='SECURITYADMIN')
    are checked against their bcrypt password_hash; employee-type rows
    (usertype='INDIVIDUAL') don't have a hash yet, so they're checked as
    plain text for now, per the payroll team's current setup.

    Returns the row as a dict, or None if the credentials don't match. For
    an INDIVIDUAL (employee) row, `userid` IS the employee's empid - that's
    how the view is built. For a SECURITYADMIN row, `userid` is the numeric
    USERS.userid and there is no empid.
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
