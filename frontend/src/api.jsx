// src/api.jsx
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const getAccessToken = () => localStorage.getItem("access_token");
const getRefreshToken = () => localStorage.getItem("refresh_token");

const axiosInstance = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) config.headers["Authorization"] = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    const shouldRetry =
      error.response?.status === 401 &&
      !originalRequest._retry &&
      getRefreshToken();

    if (shouldRetry) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(`${API_BASE}/auth/refresh/`, {
          refresh: getRefreshToken(),
        });

        const newToken = res.data.access;
        localStorage.setItem("access_token", newToken);

        axiosInstance.defaults.headers["Authorization"] = `Bearer ${newToken}`;
        originalRequest.headers["Authorization"] = `Bearer ${newToken}`;

        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error("Refresh token failed", refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;