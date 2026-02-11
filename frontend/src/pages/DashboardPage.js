import { useState } from "react";
import { motion } from "framer-motion";
import { uploadAadhaar, runPrediction } from "../services/api";
import SeverityMeter from "../components/SeverityMeter";
import HistoryTimeline from "../components/HistoryTimeline";

export default function DashboardPage({ user, onLogout }) {
  const [file, setFile] = useState(null);
  const [uploadMeta, setUploadMeta] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const meta = await uploadAadhaar(file);
      setUploadMeta(meta);
      const prediction = await runPrediction(meta.uploadId);
      setResult(prediction);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="lab-grid-bg min-h-screen px-6 py-5">
      <header className="flex items-center justify-between mb-4">
        <div>
          <div className="lab-noir-heading text-xs tracking-[0.4em] text-slate-500">
            AADHAAR FORENSICS LAB
          </div>
          <div className="mt-1 text-sm text-slate-400">
            Logged in as{" "}
            <span className="text-lab-accent">{user.email}</span>
            {user.isAdmin && " · admin"}
          </div>
        </div>
        <button
          onClick={onLogout}
          className="text-xs text-slate-400 hover:text-slate-200 border border-slate-600 rounded-full px-3 py-1"
        >
          Terminate session
        </button>
      </header>
      <div className="grid lg:grid-cols-[2fr,1.4fr] gap-4 items-start">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          className="lab-panel p-4 space-y-4"
        >
          <div className="flex justify-between items-center">
            <span className="lab-mono-label text-[0.6rem] text-slate-400">
              UPLOAD AADHAAR SNAPSHOT
            </span>
            <span className="text-[0.65rem] text-slate-500">
              ELA · ROI · Grad-CAM
            </span>
          </div>
          <div className="flex gap-3 items-center text-xs">
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="text-[0.7rem] text-slate-200"
            />
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="lab-glow-ring bg-lab-accent text-slate-900 text-[0.7rem] px-3 py-1.5 rounded-full lab-mono-label tracking-[0.2em] disabled:opacity-60"
            >
              {loading ? "ANALYSING..." : "RUN ANALYSIS"}
            </button>
          </div>
          {result && (
            <div className="grid md:grid-cols-2 gap-4 mt-3">
              <div className="space-y-3">
                <SeverityMeter
                  severity={result.severity}
                  ensembleScore={result.ensembleScore}
                  tamperedRatio={result.tamperedRatio}
                />
                <div className="text-[0.7rem] text-slate-400 space-y-1">
                  <div>DenseNet score: {(result.densenetScore * 100).toFixed(1)}%</div>
                  <div>MobileNet score: {(result.mobilenetScore * 100).toFixed(1)}%</div>
                  <div>QR valid: {result.qrValid ? "yes" : "no"}</div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="lab-mono-label text-[0.6rem] text-slate-400">
                  HEATMAP OVERLAY
                </div>
                <div className="aspect-video rounded-lg overflow-hidden border border-slate-700/80 bg-slate-950/60">
                  {result.heatmapFull && (
                    <img
                      src={`file://${result.heatmapFull}`}
                      alt="Grad-CAM heatmap"
                      className="w-full h-full object-cover"
                    />
                  )}
                </div>
              </div>
            </div>
          )}
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
          className="lab-panel p-4 space-y-3"
        >
          <div className="flex justify-between items-center">
            <span className="lab-mono-label text-[0.6rem] text-slate-400">
              HISTORY TIMELINE
            </span>
            <span className="text-[0.65rem] text-slate-500">
              Live from Convex
            </span>
          </div>
          <HistoryTimeline userId={user._id} />
        </motion.div>
      </div>
    </div>
  );
}

