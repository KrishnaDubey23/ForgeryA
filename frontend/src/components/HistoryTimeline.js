import { useQuery } from "convex/react";
import { motion } from "framer-motion";

export default function HistoryTimeline({ userId }) {
  // Use string function path to avoid importing generated API files outside src.
  const history = useQuery(
    "predictions:getHistoryByUser",
    userId ? { userId } : "skip"
  );

  if (!userId) {
    return null;
  }

  if (history === undefined) {
    return (
      <div className="text-xs text-slate-500">
        Streaming history from Convex…
      </div>
    );
  }

  if (!history.length) {
    return (
      <div className="text-xs text-slate-500">
        No analysed Aadhaar documents yet.
      </div>
    );
  }

  return (
    <div className="space-y-3 max-h-64 overflow-y-auto pr-1">
      {history.map((item, idx) => (
        <motion.div
          key={item.upload._id}
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.03 }}
          className="flex gap-3 text-xs"
        >
          <div className="w-1 bg-lab-accent-soft rounded-full mt-1" />
          <div className="flex-1 border border-slate-700/80 rounded-lg px-3 py-2.5 bg-slate-950/40">
            <div className="flex justify-between mb-1">
              <span className="lab-mono-label text-[0.6rem] text-slate-400">
                {new Date(item.upload.createdAt * 1000).toLocaleString()}
              </span>
              <span className="text-[0.65rem] text-slate-300">
                {item.prediction.severity}
              </span>
            </div>
            <div className="flex justify-between text-[0.65rem] text-slate-400">
              <span>Aadhaar capture</span>
              <span>
                Ensemble: {(item.prediction.ensembleScore * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

