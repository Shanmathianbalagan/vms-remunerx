import { useState } from "react";
import Layout from "../components/Layout";
import { checkIn, checkOut } from "../services/api";
import "./Dashboard.css";
import "./Invitation.css";
import "./CheckIn.css";

export default function CheckIn() {
  const [mode, setMode] = useState("CHECK_IN");
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function switchMode(newMode) {
    setMode(newMode);
    setResult(null);
    setError("");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!code.trim()) return;

    setSubmitting(true);
    setError("");
    setResult(null);

    try {
      const data =
        mode === "CHECK_IN" ? await checkIn(code.trim()) : await checkOut(code.trim());
      setResult(data);
      setCode("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Layout>
      <h1 className="page-title">Check-in</h1>
      <p className="page-subtitle">
        Enter the visitor's invitation code to check them in or out.
      </p>

      <div className="checkin-tabs">
        <button
          type="button"
          className={`checkin-tab ${mode === "CHECK_IN" ? "active" : ""}`}
          onClick={() => switchMode("CHECK_IN")}
        >
          Check In
        </button>
        <button
          type="button"
          className={`checkin-tab ${mode === "CHECK_OUT" ? "active" : ""}`}
          onClick={() => switchMode("CHECK_OUT")}
        >
          Check Out
        </button>
      </div>

      <form className="checkin-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Paste or type the invitation code..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
          autoFocus
        />
        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting
            ? "Processing..."
            : mode === "CHECK_IN"
            ? "Check In"
            : "Check Out"}
        </button>
      </form>

      {error && <div className="visits-error">{error}</div>}

      {result && (
        <div className="checkin-result">
          <div className="checkin-result-header">
            <i className="fa-solid fa-circle-check"></i>
            {mode === "CHECK_IN" ? "Checked in successfully" : "Checked out successfully"}
          </div>
          <div className="checkin-detail-row">
            <span className="invitation-label">Visitor</span>
            <span className="invitation-value">
              {result.visitor.name}
              {result.visitor.company ? ` · ${result.visitor.company}` : ""}
            </span>
          </div>
          <div className="checkin-detail-row">
            <span className="invitation-label">Purpose</span>
            <span className="invitation-value">{result.purpose}</span>
          </div>
          <div className="checkin-detail-row">
            <span className="invitation-label">Location</span>
            <span className="invitation-value">{result.location.name}</span>
          </div>
          <div className="checkin-detail-row">
            <span className="invitation-label">
              {mode === "CHECK_IN" ? "Checked in at" : "Checked out at"}
            </span>
            <span className="invitation-value">
              {result.checked_in_at || result.checked_out_at}
            </span>
          </div>
          <div className="checkin-detail-row">
            <span className="invitation-label">Badge</span>
            <span className="invitation-value invitation-code">
              {result.badge_code} ({result.badge_status})
            </span>
          </div>
        </div>
      )}
    </Layout>
  );
}
