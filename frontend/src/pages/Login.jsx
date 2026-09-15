import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";
import { saveSession } from "../services/auth";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(email, password);
      saveSession(data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Invalid Email or Password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-container">
      <div className="login-left">
        <h1>Welcome Back</h1>
        <p className="login-tagline">
          Sign in to continue to your Remunerx workspace.
        </p>

        <div className="login-features">
          <div>
            <i className="fa-solid fa-user-check"></i>
            Face Recognition Attendance
          </div>
          <div>
            <i className="fa-solid fa-wallet"></i>
            Accurate Payroll Processing
          </div>
          <div>
            <i className="fa-solid fa-shield-halved"></i>
            Statutory Compliance
          </div>
          <div>
            <i className="fa-solid fa-chart-line"></i>
            Reports &amp; Analytics
          </div>
        </div>
      </div>

      <div className="login-right">
        <form className="login-card" onSubmit={handleSubmit}>
          <h2>Sign In</h2>
          <p className="login-subtitle">
            Enter your credentials to access your account.
          </p>

          <div className="form-group">
            <label>Email</label>
            <div className="input-wrapper">
              <i className="fa-solid fa-envelope"></i>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-wrapper">
              <i className="fa-solid fa-lock"></i>
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <i
                className={`fa-solid toggle-password ${showPassword ? "fa-eye-slash" : "fa-eye"}`}
                onClick={() => setShowPassword((v) => !v)}
              ></i>
            </div>
          </div>

          <div className="login-options">
            <label>
              <input type="checkbox" />
              Remember Me
            </label>
            <a href="#">Forgot Password?</a>
          </div>

          {error && <div className="login-message">{error}</div>}

          <button type="submit" className="btn-login" disabled={loading}>
            <i className="fa-solid fa-right-to-bracket"></i>
            {loading ? "Signing In..." : "Sign In"}
          </button>

          {loading && (
            <div id="progressBarContainer">
              <div id="progressBar" className="progress-indeterminate"></div>
            </div>
          )}

          <div className="login-footer">© 2026 Remunerx</div>
        </form>
      </div>
    </div>
  );
}
