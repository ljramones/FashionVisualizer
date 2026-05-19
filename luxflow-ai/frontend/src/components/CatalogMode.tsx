import { useEffect, useState } from "react";
import { api } from "../api";
import type { CatalogSampleEntry } from "../types/catalog";
import CatalogGrid from "./CatalogGrid";

export default function CatalogMode() {
  const [entries, setEntries] = useState<CatalogSampleEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .catalog()
      .then((catalog) => setEntries(catalog.entries))
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <section className="mode-panel">
      <div className="section-heading">
        <h2>Catalog</h2>
        <span>{entries.length} curated entries</span>
      </div>
      {error ? <p className="error">{error}</p> : <CatalogGrid entries={entries} />}
    </section>
  );
}
