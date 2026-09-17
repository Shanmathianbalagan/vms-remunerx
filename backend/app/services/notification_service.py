from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.visit import Visit

# Notification types (see database/schema.sql / project spec):
# VISIT_INVITATION, VISIT_REMINDER, APPROVAL_NOTIFICATION, CHECK_IN_NOTIFICATION, HOST_ASSIGNED


def send_email(recipient: str, subject: str, body: str) -> bool:
    """
    Stub: no SMTP account is configured yet, so this does not actually send
    anything. Once real SMTP credentials are added (see .env), replace this
    function's body with an smtplib call and nothing else needs to change.
    """
    return False


def send_whatsapp(recipient: str, message: str) -> bool:
    """
    Stub: no WhatsApp Business API account is configured yet (e.g. Twilio or
    Meta's WhatsApp Cloud API), so this does not actually send anything. Once
    real credentials are added (see .env), replace this function's body with
    the provider's API call and nothing else needs to change.
    """
    return False


def create_notification(
    db: Session,
    visit: Visit,
    notification_type: str,
    channel: str = "EMAIL",
    recipient: str | None = None,
) -> Notification:
    if recipient is None:
        recipient = visit.visitor.phone if channel == "WHATSAPP" else visit.visitor.email

    notification = Notification(
        visit_id=visit.visit_id,
        type=notification_type,
        channel=channel,
        recipient=recipient,
        status="PENDING",
    )

    if recipient:
        message = f"You are invited to visit on {visit.start_date} at {visit.start_time}."
        if channel == "WHATSAPP":
            sent = send_whatsapp(recipient=recipient, message=message)
            notification.status = "SENT" if sent else "PENDING_WHATSAPP_SETUP"
        else:
            sent = send_email(
                recipient=recipient,
                subject=f"Visit Invitation - {visit.purpose}",
                body=message,
            )
            notification.status = "SENT" if sent else "PENDING_EMAIL_SETUP"
    else:
        notification.status = "SKIPPED_NO_" + ("PHONE" if channel == "WHATSAPP" else "EMAIL")

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
