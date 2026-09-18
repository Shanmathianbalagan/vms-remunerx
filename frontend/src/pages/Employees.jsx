import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { getEmployees } from "../services/api";
import "./Dashboard.css";
import "./Employees.css";

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getEmployees()
      .then(setEmployees)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = employees.filter((emp) => {
    const term = search.trim().toLowerCase();
    if (!term) return true;
    return (
      emp.name.toLowerCase().includes(term) ||
      (emp.email || "").toLowerCase().includes(term) ||
      (emp.department || "").toLowerCase().includes(term)
    );
  });

  return (
    <Layout>
      <h1 className="page-title">Employees</h1>
      <p className="page-subtitle">All employees in your organization.</p>

      {error && <div className="visits-error">{error}</div>}

      <input
        type="text"
        className="employees-search"
        placeholder="Search by name, email, or department..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {loading ? (
        <div className="visits-loading">Loading employees...</div>
      ) : filtered.length === 0 ? (
        <div className="visit-table-empty">No employees found.</div>
      ) : (
        <div className="visit-table-wrapper">
          <table className="visit-table">
            <thead>
              <tr>
                <th>Employee ID</th>
                <th>Employee Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Department</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((emp) => (
                <tr key={emp.employee_id}>
                  <td>{emp.employee_id}</td>
                  <td>{emp.name}</td>
                  <td>{emp.email || "-"}</td>
                  <td>{emp.phone || "-"}</td>
                  <td>{emp.department || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  );
}
