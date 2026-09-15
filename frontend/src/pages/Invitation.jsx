import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Layout from "../components/Layout";
import { getInvitation, getNotifications } from "../services/api";
import "./Dashboard.css";
import "./Invitation.css";

const NOTIFICATION_MESSAGES = {
  SENT: (n) => `Email sent to ${n.recipient}`,
  PENDING_EMAIL_SETUP: (n) =>
    `Queued for ${n.recipient} — email sending isn't connected yet, so this hasn't gone out.`,
  SKIPPED_NO_EMAIL: () => "Not sent — this visitor has no email on file.",
};

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
              <i className="fa-solid fa-envelope"></i>
              <span>{(NOTIFICATION_MESSAGES[n.status] || (() => n.status))(n)}</span>
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
