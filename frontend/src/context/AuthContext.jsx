import { createContext, useContext, useState, useEffect } from 'react';
import API from '../api/axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      API.get('/auth/me')
        .then((res) => setUser(res.data))
        .catch(() => logout())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const res = await API.post('/auth/login', formData);
    localStorage.setItem('token', res.data.access_token);
    
    const userRes = await API.get('/auth/me');
    setUser(userRes.data);
  };

  const register = async (userData) => {
  // Asegúrate de enviar name, email y password
  const response = await API.post("/auth/register", {
    name: userData.name || userData.username,
    email: userData.email,
    password: userData.password,
  });
  return response.data;
};

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);