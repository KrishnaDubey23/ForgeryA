import { useState } from "react";
import LandingPage from "./pages/LandingPage";
import DashboardPage from "./pages/DashboardPage";
import AdminPage from "./pages/AdminPage";
import { useAuth } from "./hooks/useAuth";

function App() {
  const [stage, setStage] = useState("landing"); // landing | dashboard | admin
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="lab-grid-bg min-h-screen flex items-center justify-center text-slate-300 text-xs">
        Booting forensic node…
      </div>
    );
  }

  // Demo user for testing
  const demoUser = {
    _id: "demo_user_123",
    email: "demo@forgerydetection.ai",
    isAdmin: true,
  };

  const currentUser = user || demoUser;

  if (stage === "landing") {
    return <LandingPage onGetStarted={() => setStage("dashboard")} />;
  }

  if (stage === "admin" && currentUser.isAdmin) {
    return <AdminPage user={currentUser} onBack={() => setStage("dashboard")} />;
  }

  return (
    <DashboardPage
      user={currentUser}
      onLogout={() => {
        setStage("landing");
      }}
      onOpenAdmin={currentUser.isAdmin ? () => setStage("admin") : undefined}
    />
  );
}

export default App;

