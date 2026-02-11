import { motion } from "framer-motion";

export default function LandingPage({ onGetStarted }) {
  return (
    <div className="lab-grid-bg min-h-screen flex items-center justify-center px-6 py-10">
      <motion.div
        initial={{ opacity: 0, y: 32 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.9, ease: "easeOut" }}
        className="lab-panel max-w-4xl w-full px-10 py-12 relative overflow-hidden"
      >
        <div className="absolute -top-32 -right-32 w-80 h-80 rounded-full lab-glow-ring opacity-40 blur-3xl" />
        <header className="flex items-center justify-between mb-10 relative z-10">
          <div>
            <div className="lab-noir-heading text-sm tracking-[0.35em] text-slate-400">
              AADHAAR FORENSICS
            </div>
            <h1 className="mt-3 text-4xl md:text-5xl font-semibold text-slate-50">
              Deepfake-proof{" "}
              <span className="text-lab-accent">document integrity lab</span>.
            </h1>
          </div>
          <div className="hidden md:flex flex-col items-end text-right">
            <span className="lab-mono-label text-xs text-slate-500">
              SESSION STATUS
            </span>
            <span className="mt-1 inline-flex items-center gap-2 text-emerald-400 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              NODE ONLINE
            </span>
          </div>
        </header>

        <div className="grid md:grid-cols-[2fr,1.4fr] gap-10 items-center relative z-10">
          <motion.div
            initial={{ opacity: 0, x: -24 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.15, duration: 0.7 }}
          >
            <p className="text-slate-300 text-sm md:text-base leading-relaxed">
              Every forged Aadhaar leaves a spectral fingerprint. This lab
              fuses{" "}
              <span className="text-lab-accent">
                DenseNet121, MobileNetV2 and Grad-CAM
              </span>{" "}
              to expose tampered pixels, QR inconsistencies and micro-text
              anomalies—rendered as cinematic heatmaps in real time.
            </p>
            <div className="mt-6 grid grid-cols-3 gap-3 text-xs text-slate-300">
              <div className="border border-slate-700/80 rounded-lg p-3 bg-slate-900/40">
                <div className="lab-mono-label text-[0.6rem] text-slate-500 mb-1">
                  PIPELINE
                </div>
                <div>ELA · ROI · Grad-CAM</div>
              </div>
              <div className="border border-slate-700/80 rounded-lg p-3 bg-slate-900/40">
                <div className="lab-mono-label text-[0.6rem] text-slate-500 mb-1">
                  ENSEMBLE
                </div>
                <div>DenseNet + MobileNet</div>
              </div>
              <div className="border border-slate-700/80 rounded-lg p-3 bg-slate-900/40">
                <div className="lab-mono-label text-[0.6rem] text-slate-500 mb-1">
                  SEVERITY
                </div>
                <div>Authentic → Complete Forgery</div>
              </div>
            </div>
            <div className="mt-8 flex flex-wrap items-center gap-4">
              <motion.button
                whileHover={{ scale: 1.03, boxShadow: "0 0 40px rgba(24,255,213,0.35)" }}
                whileTap={{ scale: 0.98 }}
                onClick={onGetStarted}
                className="lab-glow-ring bg-lab-accent text-slate-900 font-semibold px-7 py-3 rounded-full text-sm lab-mono-label tracking-[0.2em]"
              >
                INITIATE ANALYSIS
              </motion.button>
              <span className="text-xs text-slate-400">
                JWT-secured · Convex-backed · PyTorch inference
              </span>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 24 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.25, duration: 0.7 }}
            className="relative"
          >
            <div className="lab-panel border-slate-700/80 p-4">
              <div className="flex justify-between items-center mb-3">
                <span className="lab-mono-label text-[0.6rem] text-slate-500">
                  HEATMAP PREVIEW
                </span>
                <span className="text-[0.6rem] text-lab-accent">
                  LIVE GRAD-CAM FEED
                </span>
              </div>
              <div className="aspect-video rounded-xl overflow-hidden border border-slate-700/80 relative bg-gradient-to-br from-slate-900 via-slate-800 to-black">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_10%_0%,rgba(24,255,213,0.18),transparent_55%),radial-gradient(circle_at_90%_100%,rgba(56,189,248,0.24),transparent_60%)]" />
                <div className="absolute inset-6 border border-slate-700/70 rounded-lg" />
                <div className="absolute inset-8 border border-lab-accent-soft rounded-lg" />
                <div className="absolute left-8 top-8 w-2 h-2 rounded-full bg-lab-accent animate-ping" />
                <div className="absolute bottom-6 left-6 right-6 h-1.5 rounded-full lab-severity-meter-track opacity-80" />
              </div>
              <div className="mt-3 flex justify-between text-[0.65rem] text-slate-400">
                <span>DenseNet / MobileNet ensemble in watch-mode</span>
                <span>Convex history streaming</span>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}

