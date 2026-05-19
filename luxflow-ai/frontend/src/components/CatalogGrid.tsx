import type { CatalogSampleEntry } from "../types/catalog";
import CatalogCard from "./CatalogCard";

interface CatalogGridProps {
  entries: CatalogSampleEntry[];
}

export default function CatalogGrid({ entries }: CatalogGridProps) {
  return (
    <div className="catalog-grid">
      {entries.map((entry) => (
        <CatalogCard key={entry.id} entry={entry} />
      ))}
    </div>
  );
}
