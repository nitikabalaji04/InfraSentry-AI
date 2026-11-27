const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    options
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Something went wrong. Please try again."
    );
  }

  return data;
}

export const checkHealth = () =>
  request("/health");

export const getSummary = () =>
  request("/api/analytics/summary");

export const getScans = () =>
  request("/api/scans");

export const getScanDetails = (id) =>
  request(`/api/scans/${id}`);

export const getFileTypes = () =>
  request("/api/analytics/file-types");

export const getFindings = (severity = "") =>
  request(
    `/api/analytics/findings${
      severity ? `?severity=${encodeURIComponent(severity)}` : ""
    }`
  );

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return request("/api/upload", {
    method: "POST",
    body: formData,
  });
};

export const updateScan = (id, filename) =>
  request(`/api/scans/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ filename }),
  });

export const deleteScan = (id) =>
  request(`/api/scans/${id}`, {
    method: "DELETE",
  });