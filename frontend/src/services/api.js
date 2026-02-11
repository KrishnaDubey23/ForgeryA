import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("jwt");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Enhance error messages
    if (error.response) {
      // Backend responded with error
      const data = error.response.data;
      const message = data?.detail || data?.message || error.message;
      error.message = message;
    } else if (error.request) {
      // Request made but no response
      error.message = `Network Error: Cannot reach ${API_BASE_URL}. Is the backend running?`;
    } else {
      error.message = `Error: ${error.message}`;
    }
    return Promise.reject(error);
  }
);

export async function register(email, password, isAdmin = false) {
  const res = await apiClient.post("/auth/register", {
    email,
    password,
    isAdmin,
  });
  const token = res.data.access_token;
  localStorage.setItem("jwt", token);
  return token;
}

export async function login(email, password) {
  const res = await apiClient.post("/auth/login", { email, password });
  const token = res.data.access_token;
  localStorage.setItem("jwt", token);
  return token;
}

export async function me() {
  const res = await apiClient.get("/auth/me");
  return res.data;
}

export async function uploadAadhaar(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await apiClient.post("/uploads/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function runPrediction(uploadId) {
  const res = await apiClient.post("/predictions/", { uploadId });
  return res.data;
}

export async function getMetrics() {
  const res = await apiClient.get("/admin/metrics");
  return res.data;
}

export async function triggerRetrain() {
  const res = await apiClient.post("/admin/retrain");
  return res.data;
}

export async function demoLogin() {
  const res = await apiClient.post("/auth/demo");
  const token = res.data.access_token;
  localStorage.setItem("jwt", token);
  return token;
}

export function logout() {
  localStorage.removeItem("jwt");
}

