import { useEffect, useState } from "react";
import axiosInstance from "../api";

export default function BookingHistory() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchBookings = async () => {
      const token = localStorage.getItem("access");
      if (!token) {
        setError("⚠️ Please log in to view your bookings.");
        setLoading(false);
        return;
      }

      try {
        const { data } = await axiosInstance.get("/api/bookings/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setBookings(data);
      } catch (err) {
        const status = err.response?.status;
        if (status === 401 || status === 403) {
          setError("Session expired or unauthorized. Please log in again.");
        } else {
          setError(err.response?.data?.error || "Failed to fetch bookings.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <p className="text-blue-600 font-semibold animate-pulse">
          Loading booking history...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-xl mx-auto mt-10 p-5 bg-red-100 border border-red-300 text-red-700 rounded-xl text-center shadow-sm">
        {error}
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 p-8 bg-white rounded-2xl shadow-lg border border-gray-100">
      <h2 className="text-2xl font-bold text-blue-600 mb-6 text-center">
        My Bookings
      </h2>

      {bookings.length === 0 ? (
        <p className="text-gray-600 text-center">No bookings found.</p>
      ) : (
        <ul className="space-y-5">
          {bookings.map((booking) => {
            const dateTime = new Date(booking.created_at).toLocaleString("en-IN", {
              day: "numeric",
              month: "short",
              year: "numeric",
              hour: "2-digit",
              minute: "2-digit",
            });

            return (
              <li
                key={booking.id}
                className="p-5 bg-gray-50 border-l-4 border-blue-500 rounded-lg shadow-sm hover:shadow-md transition duration-200"
              >
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-semibold text-gray-800 capitalize">
                    {booking.vehicle_choice || "—"}
                  </h3>
                  <span className="text-green-700 font-bold">
                    ₹{Number(booking.fare ?? 0).toFixed(2)}
                  </span>
                </div>

                <p className="text-gray-700 mt-1">
                  <strong>Pickup:</strong> {booking.pickup_location}
                </p>
                <p className="text-gray-700">
                  <strong>Drop:</strong> {booking.drop_location}
                </p>

                {booking.distance_km && (
                  <p className="text-gray-700">
                    <strong>Distance:</strong> {booking.distance_km} km
                  </p>
                )}

                <p className="text-gray-500 text-sm mt-2">{dateTime}</p>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
