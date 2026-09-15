import { useNavigate } from "react-router-dom";
import { logout } from "../services/auth";
import "./Header.css";

export default function Header() {
  const navigate = useNavigate();
  const name = sessionStorage.getItem("name") || "Employee";
  const role = sessionStorage.getItem("role") || "";

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="app-header">
      <div className="header-spacer"></div>
      <div className="header-user">
        <div className="header-user-info">
          <span className="header-user-name">{name}</span>
          <span className="header-user-role">{role}</span>
        </div>
        <button className="header-logout" onClick={handleLogout}>
          <i className="fa-solid fa-right-from-bracket"></i>
          Logout
        </button>
      </div>
    </header>
  );
}
