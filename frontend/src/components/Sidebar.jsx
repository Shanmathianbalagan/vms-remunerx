import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: "fa-gauge" },
  { to: "/visits", label: "Visits", icon: "fa-calendar-check" },
  { to: "/visitors", label: "Visitors", icon: "fa-id-card" },
  { to: "/approvals", label: "Approvals", icon: "fa-check-double" },
  { to: "/check-in", label: "Check-in", icon: "fa-door-open" },
  { to: "/reports", label: "Reports", icon: "fa-chart-line" },
  { to: "/settings", label: "Settings", icon: "fa-gear" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">Remunerx VMS</div>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              "sidebar-link" + (isActive ? " active" : "")
            }
          >
            <i className={`fa-solid ${item.icon}`}></i>
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
