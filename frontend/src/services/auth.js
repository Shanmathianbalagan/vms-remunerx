export function saveSession(data) {
  sessionStorage.setItem("access_token", data.access_token);
  sessionStorage.setItem("user_id", data.user_id);
  sessionStorage.setItem("employee_id", data.employee_id);
  sessionStorage.setItem("name", data.name || "");
  sessionStorage.setItem("email", data.email);
  sessionStorage.setItem("role", data.role);
}

export function getToken() {
  return sessionStorage.getItem("access_token");
}

export function isLoggedIn() {
  return Boolean(getToken());
}

export function logout() {
  sessionStorage.clear();
}
