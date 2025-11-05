import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../api";

export default function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      const res = await axiosInstance.post("/api/auth/register/", formData);

      if (res.status === 201 || res.status === 200) {
        setMessage("✅ Registration successful! Redirecting to login...");
        setTimeout(() => navigate("/login"), 1500);
      } else {
        setMessage("⚠️ Unexpected response. Please try again.");
      }
    } catch (err) {
      const data = err.response?.data || {};
      const errorMsg =
        data.username?.[0] ||
        data.email?.[0] ||
        data.password?.[0] ||
        data.detail ||
        "❌ Failed to register!";

      setMessage(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white shadow-lg rounded-2xl p-6 mt-10">
      <h2 className="text-2xl font-bold text-blue-600 mb-4 text-center">
        Create Account
      </h2>

      {message && (
        <p
          className={`mb-4 text-center font-medium ${
            message.startsWith("✅") ? "text-green-600" : "text-red-600"
          }`}
        >
          {message}
        </p>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="Username"
          required
          className="input"
        />

        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
          required
          className="input"
        />

        <input
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Password"
          required
          className="input"
        />

        <button
          type="submit"
          disabled={loading}
          className="btn-blue w-full disabled:opacity-50"
        >
          {loading ? "Registering..." : "Register"}
        </button>
      </form>
    </div>
  );
}
