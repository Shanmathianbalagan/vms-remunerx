import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import VisitTable from "../components/VisitTable";
import { getVisits } from "../services/api";
import "./Dashboard.css";
import "./Visits.css";

const STATUS_OPTIONS = [
  "CREATED",
  "PENDING_APPROVAL",
  "APPROVED",
  "REJECTED",
  "CANCELLED",
  "COMPLETED",
];

export default function Visits() {
  const navigate = useNavigate();
  const [visits, setVisits] = useState([]);
  const [search, setSearch] = useState("");
  const [visitDate, setVisitDate] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadVisits();
  }, []);

  async function loadVisits(filters = {}) {
    setLoading(true);
    setError("");
    try {
      const data = await getVisits(filters);
      setVisits(data);
    } catch (err) {
      setError(err.message || "Failed to load visits");
    } finally {
      setLoading(false);
    }
  }

  function handleFilter(e) {
    e.preventDefault();
    loadVisits({ search, visitDate, status });
  }

  return (
    <Layout>
      <div className="visits-header">
        <div>
          <h1 className="page-title">Visits</h1>
          <p className="page-subtitle">Visits you are hosting.</p>
        </div>
        <button className="btn-primary" onClick={() => navigate("/visits/new")}>
          + Host a Visit
        </button>
      </div>

      <form className="visits-filters" onSubmit={handleFilter}>
        <input
          type="text"
          placeholder="Search visitor name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <input
          type="date"
          value={visitDate}
          onChange={(e) => setVisitDate(e.target.value)}
        />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          {STATUS_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s.replace("_", " ")}
            </option>
          ))}
        </select>
        <button type="submit" className="btn-secondary">
          Filter
        </button>
      </form>

      {error && <div className="visits-error">{error}</div>}

      {loading ? (
        <div className="visits-loading">Loading visits...</div>
      ) : (
        <VisitTable visits={visits} />
      )}
    </Layout>
  );
}
