from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.visit import Visit

# Notification types (see database/schema.sql / project spec):
# VISIT_INVITATION, VISIT_REMINDER, APPROVAL_NOTIFICATION, CHECK_IN_NOTIFICATION


def send_email(recipient: str, subject: str, body: str) -> bool:
    """
    Stub: no SMTP account is configured yet, so this does not actually send
    anything. Once real SMTP credentials are added (see .env), replace this
    function's body with an smtplib call and nothing else needs to change.
    """
    return False


def create_notification(db: Session, visit: Visit, notification_type: str) -> Notification:
    recipient = visit.visitor.email

    notification = Notification(
        visit_id=visit.visit_id,
        type=notification_type,
        channel="EMAIL",
        recipient=recipient,
        status="PENDING",
    )

    if recipient:
        sent = send_email(
            recipient=recipient,
            subject=f"Visit Invitation - {visit.purpose}",
            body=f"You are invited to visit on {visit.start_date} at {visit.start_time}.",
        )
        notification.status = "SENT" if sent else "PENDING_EMAIL_SETUP"
    else:
        notification.status = "SKIPPED_NO_EMAIL"

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
