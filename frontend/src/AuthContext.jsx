import { createContext, useState } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const access = localStorage.getItem("access_token");
    const refresh = localStorage.getItem("refresh_token");
    const username = localStorage.getItem("username");

    return access && refresh && username
      ? { access, refresh, username }
      : null;
  });

  const loginUser = ({ access, refresh, username }) => {
    const userData = { access, refresh, username };
    setUser(userData);

    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    localStorage.setItem("username", username);
  };

  const logoutUser = () => {
    setUser(null);

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");
  };

  return (
    <AuthContext.Provider value={{ user, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};