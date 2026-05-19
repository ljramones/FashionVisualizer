import { resolveBackendUrl } from "../api";
import type { CatalogEntry } from "../types/catalog";

interface ArtifactPreviewProps {
  entry: CatalogEntry | null;
}

export default function ArtifactPreview({ entry }: ArtifactPreviewProps) {
  if (!entry) {
    return null;
  }

  const artifacts = Object.fromEntries(entry.artifacts.map((artifact) => [artifact.kind, artifact]));
  const heroUrl = resolveBackendUrl(artifacts.hero_still?.static_url);
  const compositeUrl = resolveBackendUrl(artifacts.product_locked_composite?.static_url);
  const thumbnailUrl = resolveBackendUrl(artifacts.thumbnail?.static_url);

  return (
    <section className="artifact-preview">
      <h3>Generated Placeholder Artifacts</h3>
      <div className="artifact-grid">
        <ArtifactImage title="Hero Still Placeholder" url={heroUrl} path={artifacts.hero_still?.path} />
        <ArtifactImage
          title="Product-Locked Composite Placeholder"
          url={compositeUrl}
          path={artifacts.product_locked_composite?.path}
        />
        <ArtifactImage title="Thumbnail" url={thumbnailUrl} path={artifacts.thumbnail?.path} />
      </div>
      <div className="video-placeholder">
        <strong>Video Placeholder Metadata</strong>
        <span>{artifacts.video_placeholder?.path ?? "No video placeholder returned."}</span>
      </div>
      <div className="metadata-links">
        <MetadataPath label="Catalog Entry Metadata" path={artifacts.catalog_entry?.path} />
        <MetadataPath label="Pipeline Trace" path={artifacts.pipeline_trace?.path} />
      </div>
    </section>
  );
}

function MetadataPath({ label, path }: { label: string; path?: string }) {
  return (
    <div>
      <strong>{label}</strong>
      <span>{path ?? "not returned"}</span>
    </div>
  );
}

function ArtifactImage({
  title,
  url,
  path
}: {
  title: string;
  url: string | null;
  path?: string;
}) {
  return (
    <figure className="artifact-image">
      {url ? <img src={url} alt={title} /> : <div className="missing-artifact">No preview URL</div>}
      <figcaption>
        <strong>{title}</strong>
        <span>{path}</span>
      </figcaption>
    </figure>
  );
}
