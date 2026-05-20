export function DocumentUpload() {
  return (
    <div className="utility-card">
      <p className="text-body-strong text-ink">Upload legal document</p>
      <p className="mt-2 text-caption text-ink-muted-48">Supported: PDF, TXT, DOCX. OCR intentionally disabled in base scaffold.</p>
      <input
        className="mt-5 block w-full text-caption text-ink-muted-48 file:mr-4 file:rounded-pill file:border-0 file:bg-primary file:px-5 file:py-[10px] file:text-caption file:text-on-primary file:transition-transform file:active:scale-95"
        type="file"
      />
      <button className="btn-primary mt-5">Analyze document</button>
    </div>
  );
}
