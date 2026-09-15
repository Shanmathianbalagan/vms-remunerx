import Layout from "../components/Layout";
import "./Dashboard.css";

export default function Dashboard() {
  const name = sessionStorage.getItem("name") || "Employee";

  return (
    <Layout>
      <h1 className="page-title">Welcome, {name}</h1>
      <p className="page-subtitle">
        Here's a quick overview of your visitor management workspace.
      </p>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <i className="fa-solid fa-calendar-check"></i>
          <div>
            <div className="dashboard-card-label">Visits</div>
            <div className="dashboard-card-hint">Manage hosted visits</div>
          </div>
        </div>
        <div className="dashboard-card">
          <i className="fa-solid fa-id-card"></i>
          <div>
            <div className="dashboard-card-label">Visitors</div>
            <div className="dashboard-card-hint">Search or add visitors</div>
          </div>
        </div>
        <div className="dashboard-card">
          <i className="fa-solid fa-check-double"></i>
          <div>
            <div className="dashboard-card-label">Approvals</div>
            <div className="dashboard-card-hint">Pending visit approvals</div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
