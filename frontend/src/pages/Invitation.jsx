import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Layout from "../components/Layout";
import { getInvitation, getNotifications } from "../services/api";
import "./Dashboard.css";
import "./Invitation.css";

const CHANNEL_ICONS = {
  EMAIL: "fa-solid fa-envelope",
  WHATSAPP: "fa-brands fa-whatsapp",
};

function notificationMessage(n) {
  const channelLabel = n.channel === "WHATSAPP" ? "WhatsApp" : "Email";

  if (n.status === "SENT") {
    return `${channelLabel} sent to ${n.recipient}`;
  }
  if (n.status === "PENDING_EMAIL_SETUP" || n.status === "PENDING_WHATSAPP_SETUP") {
    return `Queued for ${n.recipient} — ${channelLabel.toLowerCase()} sending isn't connected yet, so this hasn't gone out.`;
  }
  if (n.status === "SKIPPED_NO_EMAIL") {
    return "Not sent — this visitor has no email on file.";
  }
  if (n.status === "SKIPPED_NO_PHONE") {
    return "Not sent — this visitor has no phone number on file.";
  }
  return n.status;
}

export default function Invitation() {
  const { visitId } = useParams();
  const navigate = useNavigate();
  const [invitation, setInvitation] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getInvitation(visitId), getNotifications(visitId)])
      .then(([invitationData, notificationData]) => {
        setInvitation(invitationData);
        setNotifications(notificationData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [visitId]);

  return (
    <Layout>
      <h1 className="page-title">Visit Invitation</h1>
      <p className="page-subtitle">
        Share this QR code with the visitor for check-in.
      </p>

      {error && <div className="visits-error">{error}</div>}

      {loading ? (
        <div className="visits-loading">Loading invitation...</div>
      ) : (
        invitation && (
          <div className="invitation-card">
            <img
              src={invitation.qr_image}
              alt="Visit invitation QR code"
              className="invitation-qr"
            />
            <div className="invitation-details">
              <div className="invitation-row">
                <span className="invitation-label">Status</span>
                <span className="invitation-value">{invitation.status}</span>
              </div>
              <div className="invitation-row">
                <span className="invitation-label">Invitation Code</span>
                <span className="invitation-value invitation-code">
                  {invitation.qr_code}
                </span>
              </div>
              <div className="invitation-row">
                <span className="invitation-label">Expires</span>
                <span className="invitation-value">{invitation.expires_at}</span>
              </div>
            </div>
          </div>
        )
      )}

      {notifications.length > 0 && (
        <div className="notification-list">
          {notifications.map((n) => (
            <div key={n.notification_id} className="notification-item">
              <i className={CHANNEL_ICONS[n.channel] || "fa-solid fa-bell"}></i>
              <span>{notificationMessage(n)}</span>
            </div>
          ))}
        </div>
      )}

      <button className="btn-secondary" onClick={() => navigate("/visits")}>
        Back to Visits
      </button>
    </Layout>
  );
}
