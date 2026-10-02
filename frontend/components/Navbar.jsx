import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-slate-900 text-white px-6 py-4 flex justify-between items-center shadow-md">
      <Link to="/" className="text-xl font-bold tracking-wide text-indigo-400">
        EcoVideo App
      </Link>
      <div className="flex gap-4 items-center">
        {user ? (
          <>
            <span className="text-sm text-gray-300">Hola, {user.username}</span>
            <Link
              to="/upload"
              className="bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg text-sm font-medium transition"
            >
              Subir Video
            </Link>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-500 px-3 py-2 rounded-lg text-sm font-medium transition"
            >
              Cerrar Sesión
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-indigo-300 text-sm font-medium">
              Iniciar Sesión
            </Link>
            <Link
              to="/register"
              className="bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg text-sm font-medium transition"
            >
              Registrarse
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}