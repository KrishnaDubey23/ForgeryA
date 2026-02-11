import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getMetrics, triggerRetrain } from "../services/api";

export default function AdminPage({ user, onBack }) {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);

  useEffect(() => {
    getMetrics()
      .then((res) => setMetrics(res.models || []))
      .finally(() => setLoading(false));
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    try {
      await triggerRetrain();
    } finally {
      setRetraining(false);
    }
  };

  return (
    <div className="lab-grid-bg min-h-screen px-6 py-5">
      <header className="flex items-center justify-between mb-4">
        <div>
          <div className="lab-noir-heading text-xs tracking-[0.4em] text-slate-500">
            ADMIN CONSOLE
          </div>
          <div className="mt-1 text-sm text-slate-400">
            {user.email} · model governance
          </div>
        </div>
        <button
          onClick={onBack}
          className="text-xs text-slate-400 hover:text-slate-200 border border-slate-600 rounded-full px-3 py-1"
        >
          Back to dashboard
        </button>
      </header>
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="lab-panel p-5 space-y-4"
      >
        <div className="flex justify-between items-center">
          <span className="lab-mono-label text-[0.6rem] text-slate-400">
            MODEL METRICS
          </span>
          <button
            onClick={handleRetrain}
            disabled={retraining}
            className="lab-glow-ring bg-lab-accent text-slate-900 text-[0.65rem] px-3 py-1.5 rounded-full lab-mono-label tracking-[0.18em] disabled:opacity-60"
          >
            {retraining ? "RETRAINING..." : "TRIGGER RETRAIN"}
          </button>
        </div>
        {loading ? (
          <div className="text-xs text-slate-500">Loading metrics…</div>
        ) : metrics.length === 0 ? (
          <div className="text-xs text-slate-500">
            No model runs logged yet. Train via CLI or retrain button.
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-3 text-xs">
            {metrics.map((m) => (
              <div
                key={m._id}
                className="border border-slate-700/80 rounded-lg px-3 py-2.5 bg-slate-950/40"
              >
                <div className="flex justify-between mb-1">
                  <span className="text-slate-200">{m.name}</span>
                  <span className="text-slate-400">v{m.version}</span>
                </div>
                <div className="flex justify-between text-slate-400 text-[0.65rem]">
                  <span>Acc: {(m.accuracy * 100).toFixed(2)}%</span>
                  <span>F1: {(m.f1Score * 100).toFixed(2)}%</span>
                </div>
                <div className="mt-1 text-[0.6rem] text-slate-500">
                  {new Date(m.createdAt * 1000).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
}

