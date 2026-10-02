import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';

export default function Upload() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert('Selecciona un archivo de video');

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('file', file);

    try {
      setUploading(true);
      await API.post('/videos/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      navigate('/');
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al subir el video');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-slate-800 rounded-xl shadow-xl border border-slate-700">
      <h2 className="text-xl font-bold text-white mb-4">Subir Nuevo Video</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm text-gray-300 mb-1">Título</label>
          <input
            type="text"
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-900 text-white border border-slate-700 focus:outline-none focus:border-indigo-500"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-300 mb-1">Descripción</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-900 text-white border border-slate-700 focus:outline-none focus:border-indigo-500"
            rows="3"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-300 mb-1">Archivo de Video (.mp4)</label>
          <input
            type="file"
            accept="video/*"
            required
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer"
          />
        </div>
        <button
          type="submit"
          disabled={uploading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 rounded-lg transition disabled:bg-indigo-900"
        >
          {uploading ? 'Subiendo a S3...' : 'Publicar Video'}
        </button>
      </form>
    </div>
  );
}