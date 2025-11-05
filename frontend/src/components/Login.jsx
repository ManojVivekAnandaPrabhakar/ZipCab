import { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../api";
import { AuthContext } from "../AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { loginUser } = useContext(AuthContext);

  const [formData, setFormData] = useState({ username: "", password: "" });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch CSRF token once on mount
  useEffect(() => {
    axiosInstance.get("/api/csrf/").catch(() =>
      console.warn("⚠️ CSRF cookie not fetched")
    );
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const { data } = await axiosInstance.post("/api/auth/login/", formData, {
        withCredentials: true,
      });

      loginUser({ username: formData.username, ...data });
      navigate("/profile");
    } catch (err) {
      const errorMsg =
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Login failed. Please try again.";
      setMessage(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-800 text-center mb-6">
          Login
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg 
                       hover:bg-blue-700 transition duration-200 disabled:opacity-50"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {message && (
          <p className="mt-4 text-red-500 text-center font-medium">{message}</p>
        )}
      </div>
    </div>
  );
}
