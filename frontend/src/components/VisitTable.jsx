import { Link } from "react-router-dom";
import "./VisitTable.css";

function formatTime(t) {
  const [h, m] = t.split(":");
  const hour = parseInt(h, 10);
  const period = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 === 0 ? 12 : hour % 12;
  return `${displayHour}:${m} ${period}`;
}

function StatusBadge({ status }) {
  return <span className={`status-badge status-${status.toLowerCase()}`}>{status}</span>;
}

function formatDateRange(startDate, endDate) {
  return startDate === endDate ? startDate : `${startDate} → ${endDate}`;
}

export default function VisitTable({ visits, showHost = false }) {
  if (visits.length === 0) {
    return <div className="visit-table-empty">No visits found.</div>;
  }

  return (
    <div className="visit-table-wrapper">
      <table className="visit-table">
        <thead>
          <tr>
            {showHost && <th>Host</th>}
            <th>Visitor</th>
            <th>Company</th>
            <th>Purpose</th>
            <th>Location</th>
            <th>Date</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {visits.map((visit) => (
            <tr key={visit.visit_id}>
              {showHost && <td>{visit.employee.name}</td>}
              <td>{visit.visitor.name}</td>
              <td>{visit.visitor.company || "-"}</td>
              <td>{visit.purpose}</td>
              <td>
                {visit.location.name}
                {visit.meeting_room ? ` · ${visit.meeting_room.name}` : ""}
              </td>
              <td>{formatDateRange(visit.start_date, visit.end_date)}</td>
              <td>{formatTime(visit.start_time)}</td>
              <td>{formatTime(visit.end_time)}</td>
              <td>
                <StatusBadge status={visit.status} />
              </td>
              <td>
                <Link to={`/visits/${visit.visit_id}/invitation`} className="table-link">
                  Invitation
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
