interface VideoPanelProps {
  path?: string;
}

export default function VideoPanel({ path }: VideoPanelProps) {
  return (
    <div className="video-panel">
      <span>video placeholder</span>
      {path ? <small>{path}</small> : null}
    </div>
  );
}
