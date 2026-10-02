import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Credenciales incorrectas');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-slate-800 rounded-xl shadow-xl border border-slate-700">
      <h2 className="text-2xl font-bold text-white text-center mb-6">Iniciar Sesión</h2>
      
      {error && (
        <div className="bg-red-500/10 border border-red-500 text-red-400 p-3 rounded-lg mb-4 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm text-gray-300 mb-1">Correo Electrónico</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-900 text-white border border-slate-700 focus:outline-none focus:border-indigo-500"
            placeholder="usuario@mail.com"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-300 mb-1">Contraseña</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-900 text-white border border-slate-700 focus:outline-none focus:border-indigo-500"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 rounded-lg transition"
        >
          Ingresar
        </button>
      </form>

      <p className="text-gray-400 text-sm text-center mt-4">
        ¿No tienes cuenta?{' '}
        <Link to="/register" className="text-indigo-400 hover:underline">
          Regístrate aquí
        </Link>
      </p>
    </div>
  );
}