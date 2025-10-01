import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../AuthContext";

export default function Navbar() {
  const { user, logoutUser } = useContext(AuthContext);

  return (
    <nav className="bg-blue-600 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        
        
        <Link
          to="/"
          className="text-white text-2xl font-bold rounded-md px-3 py-1 hover:bg-blue-700 transition"
        >
          ZipCab
        </Link>

        
        <div className="flex items-center space-x-4">

          
          <Link
            to="/calculate-fare"
            className="bg-white text-blue-600 px-4 py-2 rounded-md font-semibold hover:bg-blue-100 transition"
          >
            Calculate Fare
          </Link>

          
          {user && (
            <>
              <Link
                to="/profile"
                className="bg-white text-blue-600 px-4 py-2 rounded-md font-semibold hover:bg-blue-100 transition"
              >
                Profile
              </Link>

              <Link
                to="/bookings"
                className="bg-white text-blue-600 px-4 py-2 rounded-md font-semibold hover:bg-blue-100 transition"
              >
                Bookings
              </Link>

              <button
                onClick={logoutUser}
                className="bg-red-500 text-white px-4 py-2 rounded-md font-semibold hover:bg-red-600 transition"
              >
                Logout
              </button>
            </>
          )}

          
          {!user && (
            <>
              <Link
                to="/login"
                className="bg-white text-blue-600 px-4 py-2 rounded-md font-semibold hover:bg-blue-100 transition"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="bg-white text-blue-600 px-4 py-2 rounded-md font-semibold hover:bg-blue-100 transition"
              >
                Register
              </Link>
            </>
          )}

        </div>
      </div>
    </nav>
  );
}