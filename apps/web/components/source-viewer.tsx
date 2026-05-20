export function SourceViewer() {
  return (
    <div className="card">
      <h3 className="text-lg font-medium">Verified Sources</h3>
      <p className="mt-2 text-sm text-body">Only sources with verification_status=verified and index_status=indexed appear here.</p>
      <div className="mt-4 rounded-md border border-hairline bg-canvas p-3 text-sm text-muted">
        Source metadata and chunk preview placeholder.
      </div>
    </div>
  );
}
