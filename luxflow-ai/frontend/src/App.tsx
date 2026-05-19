import { useState } from "react";
import Header from "./components/Header";
import CatalogMode from "./components/CatalogMode";
import WorkflowMode from "./components/WorkflowMode";

type Mode = "catalog" | "workflow";

export default function App() {
  const [mode, setMode] = useState<Mode>("catalog");

  return (
    <div className="app-shell">
      <Header mode={mode} onModeChange={setMode} />
      <main>{mode === "catalog" ? <CatalogMode /> : <WorkflowMode />}</main>
    </div>
  );
}
