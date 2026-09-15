import { Navigate, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Visits from "./pages/Visits";
import CreateVisit from "./pages/CreateVisit";
import Invitation from "./pages/Invitation";
import Approvals from "./pages/Approvals";
import ComingSoon from "./pages/ComingSoon";
import { isLoggedIn } from "./services/auth";

function PrivateRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/visits"
        element={
          <PrivateRoute>
            <Visits />
          </PrivateRoute>
        }
      />
      <Route
        path="/visits/new"
        element={
          <PrivateRoute>
            <CreateVisit />
          </PrivateRoute>
        }
      />
      <Route
        path="/visits/:visitId/invitation"
        element={
          <PrivateRoute>
            <Invitation />
          </PrivateRoute>
        }
      />
      <Route
        path="/visitors"
        element={
          <PrivateRoute>
            <ComingSoon title="Visitors" />
          </PrivateRoute>
        }
      />
      <Route
        path="/approvals"
        element={
          <PrivateRoute>
            <Approvals />
          </PrivateRoute>
        }
      />
      <Route
        path="/check-in"
        element={
          <PrivateRoute>
            <ComingSoon title="Check-in" />
          </PrivateRoute>
        }
      />
      <Route
        path="/reports"
        element={
          <PrivateRoute>
            <ComingSoon title="Reports" />
          </PrivateRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <PrivateRoute>
            <ComingSoon title="Settings" />
          </PrivateRoute>
        }
      />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
