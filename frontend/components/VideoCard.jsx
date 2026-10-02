export default function VideoCard({ video }) {
  return (
    <div className="bg-slate-800 text-white rounded-xl overflow-hidden shadow-lg border border-slate-700">
      <video
        src={video.video_url}
        controls
        className="w-full h-48 object-cover bg-black"
      />
      <div className="p-4">
        <h3 className="font-semibold text-lg text-indigo-300 mb-1">{video.title}</h3>
        <p className="text-gray-400 text-sm mb-3">{video.description}</p>
        <div className="text-xs text-gray-500 flex justify-between border-t border-slate-700 pt-2">
          <span>Por: {video.owner?.username || 'Usuario'}</span>
          <span>{new Date(video.created_at).toLocaleDateString()}</span>
        </div>
      </div>
    </div>
  );
}