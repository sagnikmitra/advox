export function SourceViewer() {
  return (
    <div className="utility-card">
      <p className="text-body-strong text-ink">Verified Sources</p>
      <p className="mt-2 text-caption text-ink-muted-48">
        Only sources with verification_status=verified and index_status=indexed appear here.
      </p>
      <div className="mt-4 rounded-lg border border-hairline bg-canvas-parchment p-4 text-caption text-ink-muted-48">
        Source metadata and chunk preview placeholder.
      </div>
    </div>
  );
}
