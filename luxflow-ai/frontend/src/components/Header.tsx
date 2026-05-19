interface HeaderProps {
  mode: "catalog" | "workflow";
  onModeChange: (mode: "catalog" | "workflow") => void;
}

export default function Header({ mode, onModeChange }: HeaderProps) {
  return (
    <header className="header">
      <div>
        <h1>LuxFlow AI</h1>
        <p>Product-preserving workflow studio for handbag catalog videos.</p>
      </div>
      <nav className="tabs" aria-label="Mode selector">
        <button className={mode === "catalog" ? "active" : ""} onClick={() => onModeChange("catalog")}>
          Catalog
        </button>
        <button className={mode === "workflow" ? "active" : ""} onClick={() => onModeChange("workflow")}>
          Workflow
        </button>
      </nav>
    </header>
  );
}
