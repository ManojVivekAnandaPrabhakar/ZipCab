import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../api";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axiosInstance.get("/api/auth/profile/");
        setProfile(res.data);
      } catch (err) {
        console.error("Profile fetch failed:", err);
        if (err.response?.status === 401) navigate("/login"); // token invalid → redirect
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  if (loading)
    return (
      <p className="text-center text-blue-500 mt-10 animate-pulse">
        Loading profile...
      </p>
    );

  if (!profile)
    return (
      <p className="text-center text-red-500 mt-10">
        Unable to load profile.
      </p>
    );

  return (
    <div className="flex justify-center mt-10">
      <div className="bg-white shadow-lg rounded-xl p-6 w-full max-w-md border-l-4 border-blue-500 hover:shadow-2xl transition-shadow duration-300">
        <h2 className="text-2xl font-bold text-blue-600 mb-4 text-center">
          Profile
        </h2>

        <div className="space-y-3 text-gray-700">
          <p>
            <span className="font-semibold text-blue-500">Username:</span>{" "}
            {profile.username}
          </p>

          <p>
            <span className="font-semibold text-blue-500">Email:</span>{" "}
            {profile.email}
          </p>

          {profile.message && (
            <p className="italic border-l-2 border-blue-200 pl-2">
              {profile.message}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
