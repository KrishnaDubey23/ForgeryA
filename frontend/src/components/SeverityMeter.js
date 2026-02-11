import { motion } from "framer-motion";

const severityOrder = ["Authentic", "Minor Tampering", "Partial Forgery", "Complete Forgery"];

export default function SeverityMeter({ severity = "Authentic", ensembleScore = 0, tamperedRatio = 0 }) {
  const index = severityOrder.indexOf(severity);
  const progress = index >= 0 ? (index / (severityOrder.length - 1)) : ensembleScore;

  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <span className="lab-mono-label text-[0.6rem] text-slate-400">
          SEVERITY INDEX
        </span>
        <span className="text-[0.65rem] text-slate-300">
          {severity} · {(ensembleScore * 100).toFixed(1)}%
        </span>
      </div>
      <div className="relative h-2 rounded-full bg-slate-800 overflow-hidden">
        <div className="absolute inset-0 lab-severity-meter-track opacity-80" />
        <motion.div
          className="absolute inset-y-0 left-0 bg-black/40"
          initial={{ width: "0%" }}
          animate={{ width: `${progress * 100}%` }}
          transition={{ duration: 0.7, ease: "easeOut" }}
        />
      </div>
      <div className="mt-1 flex justify-between text-[0.6rem] text-slate-500">
        <span>Tampered area: {(tamperedRatio * 100).toFixed(1)}%</span>
        <span>Weighted ensemble</span>
      </div>
    </div>
  );
}

