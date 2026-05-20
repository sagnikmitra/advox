export function DocumentUpload() {
  return (
    <div className="card">
      <h3 className="text-lg font-medium">Upload legal document</h3>
      <p className="mt-2 text-sm text-body">Supported: PDF, TXT, DOCX. OCR intentionally disabled in base scaffold.</p>
      <input className="mt-4 block w-full rounded-md border border-hairline bg-canvas px-3 py-2 text-sm" type="file" />
      <button className="mt-4 h-10 rounded-md bg-primary px-4 text-sm font-medium text-white">Analyze document</button>
    </div>
  );
}
