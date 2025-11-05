// src/api.jsx
import axios from "axios";
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
  setRefreshToken,
  clearTokens,
} from "./token";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const axiosInstance = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

// attach access token to outgoing requests
axiosInstance.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) config.headers["Authorization"] = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// handle 401 -> try refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Only attempt refresh once per request
    const shouldRetry =
      error.response?.status === 401 &&
      !originalRequest._retry &&
      getRefreshToken();

    if (shouldRetry) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(`${API_BASE}/api/auth/refresh/`, {
          refresh: getRefreshToken(),
        });

        const newAccess = res.data.access;
        const newRefresh = res.data.refresh || getRefreshToken(); // if rotate

        // persist tokens
        setAccessToken(newAccess);
        if (newRefresh) setRefreshToken(newRefresh);

        // update headers and retry
        axiosInstance.defaults.headers["Authorization"] = `Bearer ${newAccess}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccess}`;

        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // refresh failed -> logout client-side
        clearTokens();
        // optionally redirect to login: window.location = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
