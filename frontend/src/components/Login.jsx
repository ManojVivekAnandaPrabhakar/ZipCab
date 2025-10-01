import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../api";
import { AuthContext } from "../AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { loginUser } = useContext(AuthContext);

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await axiosInstance.post("/auth/login/", formData);

      
      loginUser({ username: formData.username, ...response.data });

      
      navigate("/profile");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Invalid credentials");
    } finally {
      setLoading(false);
    }
  }


  const errorMessage = message && (
    <p className="mt-4 text-red-500 text-center font-medium">{message}</p>
  );

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg">
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
            className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-400"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-400"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg 
                       hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        
        {errorMessage}
      </div>
    </div>
  );
}