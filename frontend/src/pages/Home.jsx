import { useContext } from "react";
import { AuthContext } from "../AuthContext";
import { Link } from "react-router-dom";

export default function Home() {
  const { user } = useContext(AuthContext);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md text-center">
        <h1 className="text-3xl font-bold text-blue-600 mb-4">Welcome to ZipCab</h1>
        {user ? (
          <>
            <p className="text-lg mb-4">Hello, <span className="font-semibold">{user.username}</span>!</p>
            <Link
              to="/calculate-fare"
              className="inline-block bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 transition duration-300"
            >
              Book a Cab
            </Link>
          </>
        ) : (
          <>
            <p className="text-lg mb-4">Please login or register to continue.</p>
            <div className="flex justify-center gap-4">
              <Link
                to="/login"
                className="bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 transition duration-300"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="bg-green-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-green-700 transition duration-300"
              >
                Register
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}