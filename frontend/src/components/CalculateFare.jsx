import { useState } from "react";
import axiosInstance from "../api";

export default function CalculateFare() {
  const [formData, setFormData] = useState({
    pickup: "",
    drop: "",
    choice: "sedan",
    mobile_number: "",
  });

  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [bookingLoading, setBookingLoading] = useState(false);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleCalculate(e) {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axiosInstance.post("/calculate-fare/", formData);
      setResult(response.data);
      setMessage("");
    } catch (err) {
      setMessage(err.response?.data?.error || "Failed to calculate fare");
    } finally {
      setLoading(false);
    }
  }

  async function handleBook() {
    if (!result) return;

    if (!/^\d{10}$/.test(formData.mobile_number)) {
      setMessage("Enter a valid 10-digit mobile number");
      return;
    }

    setBookingLoading(true);

    try {
      const response = await axiosInstance.post("/bookings/create/", {
        pickup_location: result.pickup,
        drop_location: result.drop,
        vehicle_choice: result.choice,
        mobile_number: formData.mobile_number,
      });

      alert(`Booking successful! Booking ID: ${response.data.id}`);

      
      setResult(null);
      setFormData({
        pickup: "",
        drop: "",
        choice: "sedan",
        mobile_number: "",
      });
    } catch (err) {
      alert(err.response?.data?.error || "Booking failed");
    } finally {
      setBookingLoading(false);
    }
  }


  const errorMessage = message && (
    <p className="mt-3 text-red-500 font-medium text-center">{message}</p>
  );

  const fareResult = result && (
    <div className="mt-6 p-4 bg-gray-50 rounded-xl shadow-inner space-y-2">
      <p>
        <span className="font-semibold">Pickup:</span> {result.pickup}
      </p>
      <p>
        <span className="font-semibold">Drop:</span> {result.drop}
      </p>
      <p>
        <span className="font-semibold">Vehicle:</span> {result.choice}
      </p>
      <p>
        <span className="font-semibold">Distance:</span> {result.distance_km} km
      </p>
      <p>
        <span className="font-semibold">Fare:</span> ₹{result.fare}
      </p>

      <button
        onClick={handleBook}
        disabled={bookingLoading}
        className="w-full bg-green-600 text-white py-2 rounded-lg 
                   hover:bg-green-700 transition disabled:opacity-50"
      >
        {bookingLoading ? "Booking..." : "Book Now"}
      </button>
    </div>
  );

  return (
    <div className="max-w-lg mx-auto p-6 bg-white rounded-2xl shadow-md">
      <h2 className="text-xl font-bold mb-4 text-gray-800 text-center">
        Calculate Fare & Book
      </h2>

      
      <form onSubmit={handleCalculate} className="space-y-4">
        <input
          type="text"
          name="pickup"
          placeholder="Pickup Location"
          value={formData.pickup}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-400"
        />

        <input
          type="text"
          name="drop"
          placeholder="Drop Location"
          value={formData.drop}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-400"
        />

        <select
          name="choice"
          value={formData.choice}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-400"
        >
          <option value="sedan">Sedan</option>
          <option value="suv">SUV</option>
          <option value="coupe">Coupe</option>
          <option value="mini van">Mini Van</option>
        </select>

        <input
          type="text"
          name="mobile_number"
          placeholder="Mobile Number"
          value={formData.mobile_number}
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
          {loading ? "Calculating..." : "Calculate Fare"}
        </button>
      </form>

      
      {errorMessage}
      {fareResult}
    </div>
  );
}