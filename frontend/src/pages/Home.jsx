import { useEffect, useState } from 'react';
import API from '../api/axios';
import VideoCard from '../components/VideoCard';

export default function Home() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get('/videos/')
      .then((res) => setVideos(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center mt-10 text-white">Cargando videos...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-white mb-6">Explorar Videos</h1>
      {videos.length === 0 ? (
        <p className="text-gray-400">No hay videos subidos aún.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {videos.map((video) => (
            <VideoCard key={video.id} video={video} />
          ))}
        </div>
      )}
    </div>
  );
}