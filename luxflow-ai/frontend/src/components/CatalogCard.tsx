import type { CatalogSampleEntry } from "../types/catalog";
import VideoPanel from "./VideoPanel";

interface CatalogCardProps {
  entry: CatalogSampleEntry;
}

export default function CatalogCard({ entry }: CatalogCardProps) {
  return (
    <article className="catalog-card">
      <VideoPanel path={entry.video_path} />
      <div className="card-body">
        <h3>{entry.product_name}</h3>
        <dl>
          <div>
            <dt>Model</dt>
            <dd>{entry.model}</dd>
          </div>
          <div>
            <dt>Location</dt>
            <dd>{entry.location}</dd>
          </div>
          <div>
            <dt>Action</dt>
            <dd>{entry.action}</dd>
          </div>
          <div>
            <dt>Route</dt>
            <dd>{entry.route}</dd>
          </div>
        </dl>
        <ul className="notes">
          {entry.eval_notes.map((note) => (
            <li key={note}>{note}</li>
          ))}
        </ul>
      </div>
    </article>
  );
}
