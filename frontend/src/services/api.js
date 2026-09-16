const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function login(email, password) {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
}

function authHeaders() {
  const token = sessionStorage.getItem("access_token");
  return { Authorization: `Bearer ${token}` };
}

export async function searchVisitors(q) {
  const response = await fetch(
    `${API_URL}/api/visitors/search?q=${encodeURIComponent(q)}`,
    { headers: authHeaders() }
  );
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to search visitors");
  }
  return data;
}

export async function createVisitor(visitor) {
  const response = await fetch(`${API_URL}/api/visitors`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(visitor),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to add visitor");
  }
  return data;
}

export async function getLocations() {
  const response = await fetch(`${API_URL}/api/locations`, {
    headers: authHeaders(),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to load locations");
  }
  return data;
}

export async function createVisit(visit) {
  const response = await fetch(`${API_URL}/api/visits`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(visit),
  });
  const data = await response.json();
  if (!response.ok) {
    const message = Array.isArray(data.detail)
      ? data.detail.map((d) => d.msg).join(", ")
      : data.detail;
    throw new Error(message || "Failed to create visit");
  }
  return data;
}

export async function getInvitation(visitId) {
  const response = await fetch(`${API_URL}/api/visits/${visitId}/invitation`, {
    headers: authHeaders(),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to load invitation");
  }
  return data;
}

export async function getNotifications(visitId) {
  const response = await fetch(`${API_URL}/api/visits/${visitId}/notifications`, {
    headers: authHeaders(),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to load notifications");
  }
  return data;
}

export async function getApprovals(statusFilter = "PENDING") {
  const params = new URLSearchParams();
  if (statusFilter) params.set("status", statusFilter);

  const response = await fetch(`${API_URL}/api/approvals?${params.toString()}`, {
    headers: authHeaders(),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to load approvals");
  }
  return data;
}

export async function decideApproval(approvalId, decisionStatus, comments) {
  const response = await fetch(`${API_URL}/api/approvals/${approvalId}/decide`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ status: decisionStatus, comments: comments || null }),
  });
  const data = await response.json();
  if (!response.ok) {
    const message = Array.isArray(data.detail)
      ? data.detail.map((d) => d.msg).join(", ")
      : data.detail;
    throw new Error(message || "Failed to submit decision");
  }
  return data;
}

export async function checkIn(code) {
  const response = await fetch(`${API_URL}/api/checkin`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ code }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Check-in failed");
  }
  return data;
}

export async function checkOut(code) {
  const response = await fetch(`${API_URL}/api/checkout`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ code }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Check-out failed");
  }
  return data;
}

export async function getVisits({ search, visitDate, status } = {}) {
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  if (visitDate) params.set("on_date", visitDate);
  if (status) params.set("status", status);

  const response = await fetch(`${API_URL}/api/visits?${params.toString()}`, {
    headers: authHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to load visits");
  }

  return data;
}
