interface RecipeViewerProps {
  title: string;
  data: unknown;
}

export default function RecipeViewer({ title, data }: RecipeViewerProps) {
  return (
    <section className="json-panel">
      <h3>{title}</h3>
      <pre>{data ? JSON.stringify(data, null, 2) : "No data yet."}</pre>
    </section>
  );
}
