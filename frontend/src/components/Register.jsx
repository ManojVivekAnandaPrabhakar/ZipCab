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
      // Log full error for debugging
      console.error("Registration Error:", err.response?.data || err);

      // Build a combined message for all field errors
      const data = err.response?.data || {};
      let combinedMsg = "";

      if (data.username) combinedMsg += `Username: ${data.username.join(" ")}\n`;
      if (data.email) combinedMsg += `Email: ${data.email.join(" ")}\n`;
      if (data.password) combinedMsg += `Password: ${data.password.join(" ")}\n`;
      if (data.detail) combinedMsg += `${data.detail}\n`;

      setMessage(combinedMsg.trim() || "❌ Failed to register!");
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
        <pre
          className={`mb-4 text-center font-medium whitespace-pre-wrap ${
            message.startsWith("✅") ? "text-green-600" : "text-red-600"
          }`}
        >
          {message}
        </pre>
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
