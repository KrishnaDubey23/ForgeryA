import { useEffect, useState } from "react";
import { login as apiLogin, register as apiRegister, me, logout as apiLogout, demoLogin } from "../services/api";

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [backendError, setBackendError] = useState(null);

  useEffect(() => {
    const initAuth = async () => {
      try {
        // Check if backend is reachable
        await fetch("http://localhost:8000/health").catch(() => {
          throw new Error("Backend is not accessible. Make sure the backend server is running on http://localhost:8000");
        });

        const token = localStorage.getItem("jwt");
        if (!token) {
          setLoading(false);
          return;
        }
        me()
          .then((u) => setUser(u))
          .catch(() => {
            localStorage.removeItem("jwt");
            setUser(null);
          })
          .finally(() => setLoading(false));
      } catch (error) {
        setBackendError(error.message);
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    await apiLogin(email, password);
    const u = await me();
    setUser(u);
  };

  const register = async (email, password, isAdmin = false) => {
    await apiRegister(email, password, isAdmin);
    const u = await me();
    setUser(u);
  };

  const demoMode = async () => {
    await demoLogin();
    const u = await me();
    setUser(u);
  };

  const logout = () => {
    apiLogout();
    setUser(null);
  };

  return { user, loading, login, register, logout, demoMode, backendError };
}

