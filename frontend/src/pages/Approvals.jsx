import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { getApprovals, decideApproval } from "../services/api";
import "./Dashboard.css";
import "./Approvals.css";

export default function Approvals() {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actingOn, setActingOn] = useState(null);

  useEffect(() => {
    loadApprovals();
  }, []);

  async function loadApprovals() {
    setLoading(true);
    setError("");
    try {
      const data = await getApprovals("PENDING");
      setApprovals(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDecision(approvalId, decisionStatus) {
    setActingOn(approvalId);
    setError("");
    try {
      await decideApproval(approvalId, decisionStatus);
      setApprovals((prev) => prev.filter((a) => a.approval_id !== approvalId));
    } catch (err) {
      setError(err.message);
    } finally {
      setActingOn(null);
    }
  }

  return (
    <Layout>
      <h1 className="page-title">Approvals</h1>
      <p className="page-subtitle">Visits waiting for approval.</p>

      {error && <div className="visits-error">{error}</div>}

      {loading ? (
        <div className="visits-loading">Loading approvals...</div>
      ) : approvals.length === 0 ? (
        <div className="visit-table-empty">No pending approvals.</div>
      ) : (
        <div className="approvals-list">
          {approvals.map((a) => (
            <div key={a.approval_id} className="approval-card">
              <div className="approval-info">
                <strong>{a.visit.visitor.name}</strong>
                <span className="approval-meta">
                  {a.visit.purpose} · {a.visit.location.name} ·{" "}
                  {a.visit.start_date === a.visit.end_date
                    ? a.visit.start_date
                    : `${a.visit.start_date} → ${a.visit.end_date}`}
                </span>
              </div>
              <div className="approval-actions">
                <button
                  className="btn-approve"
                  disabled={actingOn === a.approval_id}
                  onClick={() => handleDecision(a.approval_id, "APPROVED")}
                >
                  Approve
                </button>
                <button
                  className="btn-reject"
                  disabled={actingOn === a.approval_id}
                  onClick={() => handleDecision(a.approval_id, "REJECTED")}
                >
                  Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
