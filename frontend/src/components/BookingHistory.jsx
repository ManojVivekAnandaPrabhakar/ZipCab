import { useEffect, useState } from "react";
import axiosInstance from "../api";

export default function BookingHistory() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadBookings() {
      try {
        const response = await axiosInstance.get("/bookings/");
        setBookings(response.data);
      } catch (err) {
        setError(err.response?.data?.error || "Failed to fetch bookings");
      } finally {
        setLoading(false);
      }
    }

    loadBookings();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <p className="text-blue-600 font-semibold">
          Loading booking history...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-xl mx-auto mt-10 p-4 text-center 
                      bg-red-100 text-red-800 border border-red-400 
                      rounded-lg shadow-sm">
        {error}
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 p-8 bg-white 
                    shadow-lg rounded-2xl">
      <h2 className="text-3xl font-bold text-blue-600 mb-6 text-center">
        My Bookings
      </h2>

      {bookings.length === 0 ? (
        <p className="text-gray-600 text-center">No bookings yet.</p>
      ) : (
        <ul className="space-y-4">
          {bookings.map((booking) => {
            const bookingDate = new Date(booking.booking_time);
            const date = bookingDate.toLocaleDateString("en-IN", {
              day: "numeric",
              month: "short",
              year: "numeric",
            });
            const time = bookingDate.toLocaleTimeString("en-IN", {
              hour: "2-digit",
              minute: "2-digit",
            });

            return (
              <li
                key={booking.id}
                className="p-5 border-l-4 border-blue-500 
                           bg-gray-50 rounded-lg shadow-sm 
                           hover:shadow-md transition duration-300"
              >
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-semibold text-gray-800 capitalize">
                    {booking.vehicle_choice}
                  </h3>
                  <span className="text-green-700 font-bold">
                    ₹{Number(booking.fare ?? 0).toFixed(2)}
                  </span>
                </div>

                <p className="text-gray-600 mt-1">
                  <strong>Pick-up location:</strong> {booking.pickup_location}
                </p>

                <p className="text-gray-600">
                  <strong>Drop location:</strong> {booking.drop_location}
                </p>

                <p className="text-gray-600">
                  <strong>Distance:</strong> {booking.distance_km} km
                </p>

                <p className="text-gray-500 text-sm mt-2">
                  {booking.created_at
                    ? new Date(booking.created_at).toLocaleString()
                    : "No date available"}
                </p>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}