import { HashRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import { useContext } from "react";
import { AuthContext } from "./AuthContext";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Register from "./components/Register";
import Login from "./components/Login";
import Profile from "./components/Profile";
import CalculateFare from "./components/CalculateFare";
import BookingHistory from "./components/BookingHistory";

function App() {
    const { user } = useContext(AuthContext);

    const PrivateRoute = ({ children }) => {
        return user ? children : <Navigate to="/login" />;
    };

    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
                <Route path="/calculate-fare" element={<PrivateRoute><CalculateFare /></PrivateRoute>} />
                <Route path="/bookings" element={<PrivateRoute><BookingHistory /></PrivateRoute>} />
            </Routes>
        </Router>
    );
}

export default App;