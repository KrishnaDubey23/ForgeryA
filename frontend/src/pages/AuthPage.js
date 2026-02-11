import { useState } from "react";
import { motion } from "framer-motion";

export default function AuthPage({ onAuthenticated, onBack, onAuthError, auth }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "login") {
        await auth.login(email, password);
      } else {
        await auth.register(email, password, isAdmin);
      }
      onAuthenticated();
    } catch (err) {
      console.error(err);
      const errorMsg = err.response?.data?.detail || err.message || "Authentication failed";
      setError(errorMsg);
      onAuthError?.(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleDemo = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await auth.demoMode();
      onAuthenticated();
    } catch (err) {
      console.error(err);
      const errorMsg = err.response?.data?.detail || err.message || "Demo login failed";
      setError(errorMsg);
      onAuthError?.(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="lab-grid-bg min-h-screen flex items-center justify-center px-6 py-10">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="lab-panel max-w-md w-full px-8 py-8 relative"
      >
        <button
          onClick={onBack}
          className="absolute left-6 top-5 text-xs text-slate-500 hover:text-slate-300"
        >
          ⬑ Back
        </button>
        <div className="text-center mb-6">
          <div className="lab-noir-heading text-xs tracking-[0.4em] text-slate-500 mb-2">
            SECURE CONSOLE
          </div>
          <h2 className="text-2xl font-semibold text-slate-50">
            {mode === "login" ? "Log into the lab" : "Provision analyst access"}
          </h2>
        </div>
        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-900/40 border border-red-700 text-red-300 text-xs">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4 mt-4">
          <div>
            <label className="lab-mono-label text-[0.6rem] text-slate-400">
              EMAIL
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full rounded-lg bg-slate-900/60 border border-slate-700 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-lab-accent"
            />
          </div>
          <div>
            <label className="lab-mono-label text-[0.6rem] text-slate-400">
              PASSWORD
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-lg bg-slate-900/60 border border-slate-700 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-lab-accent"
            />
          </div>
          {mode === "register" && (
            <label className="flex items-center gap-2 text-xs text-slate-400">
              <input
                type="checkbox"
                checked={isAdmin}
                onChange={(e) => setIsAdmin(e.target.checked)}
                className="rounded border-slate-600 bg-slate-900 text-lab-accent"
              />
              Provision as admin (can retrain models)
            </label>
          )}
          <button
            type="submit"
            disabled={loading}
            className="mt-3 w-full lab-glow-ring bg-lab-accent text-slate-900 font-semibold py-2.5 rounded-full text-xs lab-mono-label tracking-[0.2em] disabled:opacity-50"
          >
            {loading
              ? "PROCESSING..."
              : mode === "login"
              ? "ENTER THE LAB"
              : "CREATE ANALYST PROFILE"}
          </button>
        </form>

        <div className="mt-4 border-t border-slate-700 pt-4">
          <button
            onClick={handleDemo}
            disabled={loading}
            className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs lab-mono-label tracking-[0.1em] disabled:opacity-50 transition"
          >
            SKIP TO DEMO MODE
          </button>
          <p className="text-center text-[0.65rem] text-slate-500 mt-2">
            Test drive with demo account (admin access)
          </p>
        </div>

        <div className="mt-4 text-center text-[0.7rem] text-slate-400">
          {mode === "login" ? (
            <>
              No account yet?{" "}
              <button
                className="text-lab-accent hover:underline"
                onClick={() => {
                  setMode("register");
                  setError("");
                }}
              >
                Register analyst
              </button>
            </>
          ) : (
            <>
              Already cleared?{" "}
              <button
                className="text-lab-accent hover:underline"
                onClick={() => {
                  setMode("login");
                  setError("");
                }}
              >
                Log in
              </button>
            </>
          )}
        </div>
      </motion.div>
    </div>
  );
}

