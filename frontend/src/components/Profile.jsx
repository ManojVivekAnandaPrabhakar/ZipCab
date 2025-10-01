import { useEffect, useState } from "react";
import axiosInstance from "../api";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch profile data
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axiosInstance.get("/auth/profile/");
        setProfile(res.data);
      } catch (err) {
        console.error("Failed to fetch profile:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  // Loading state
  if (loading) {
    return (
      <p className="text-center text-blue-500 mt-10 animate-pulse">
        Loading profile...
      </p>
    );
  }

  // If no profile found (just in case)
  if (!profile) {
    return (
      <p className="text-center text-red-500 mt-10">
        Unable to load profile.
      </p>
    );
  }

  // Profile UI
  return (
    <div className="flex justify-center mt-10">
      <div className="bg-white shadow-xl rounded-xl p-6 w-full max-w-md border-l-4 border-blue-500 hover:shadow-2xl transition-shadow duration-300">
        
        <h2 className="text-2xl font-bold mb-4 text-center text-blue-600">
          Profile
        </h2>

        <div className="space-y-3">
          <p>
            <span className="font-semibold text-blue-500">Username:</span>{" "}
            <span className="text-gray-800">{profile.username}</span>
          </p>

          <p>
            <span className="font-semibold text-blue-500">Email:</span>{" "}
            <span className="text-gray-800">{profile.email}</span>
          </p>

          {profile.message && (
            <p className="text-gray-600 italic border-l-2 border-blue-200 pl-2">
              {profile.message}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}