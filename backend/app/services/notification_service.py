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


_SUBJECTS = {
    "CHECK_IN_NOTIFICATION": "Your visitor has arrived",
    "HOST_ASSIGNED": "You're hosting a visit",
    "APPROVAL_NOTIFICATION": "Visit approval update",
}


def _build_message(visit: Visit, notification_type: str, qr_code: str | None = None) -> str:
    if notification_type == "CHECK_IN_NOTIFICATION":
        return f"{visit.visitor.name} has checked in and is waiting to see you ({visit.purpose})."
    if notification_type == "HOST_ASSIGNED":
        return f"You've been assigned to host {visit.visitor.name} on {visit.start_date} at {visit.start_time} ({visit.purpose})."
    if notification_type == "APPROVAL_NOTIFICATION":
        return f"Your visit request for {visit.visitor.name} on {visit.start_date} has been {visit.status.lower()}."
    if notification_type == "VISIT_INVITATION":
        message = f"You are invited to visit on {visit.start_date} at {visit.start_time}."
        if qr_code:
            message += f" Show this code at reception to check in: {qr_code}"
        return message
    return f"You are invited to visit on {visit.start_date} at {visit.start_time}."


def create_notification(
    db: Session,
    visit: Visit,
    notification_type: str,
    channel: str = "EMAIL",
    recipient: str | None = None,
    qr_code: str | None = None,
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
        message = _build_message(visit, notification_type, qr_code)
        if channel == "WHATSAPP":
            sent = send_whatsapp(recipient=recipient, message=message)
            notification.status = "SENT" if sent else "PENDING_WHATSAPP_SETUP"
        else:
            sent = send_email(
                recipient=recipient,
                subject=_SUBJECTS.get(notification_type, f"Visit Invitation - {visit.purpose}"),
                body=message,
            )
            notification.status = "SENT" if sent else "PENDING_EMAIL_SETUP"
    else:
        notification.status = "SKIPPED_NO_" + ("PHONE" if channel == "WHATSAPP" else "EMAIL")

    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
