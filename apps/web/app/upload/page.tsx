import { DocumentUpload } from "@/components/document-upload";

export default function UploadPage() {
  return (
    <>
      <section className="tile-light">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Document Analyzer.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Upload legal documents for summary, deadlines, risk radar, and verified citations.
          </p>
        </div>
      </section>

      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content space-y-6">
          <DocumentUpload />
          <div className="utility-card text-left">
            <p className="text-body-strong text-ink">Analysis output</p>
            <p className="mt-2 text-caption text-ink-muted-48">
              Includes summary, procedural history, deadlines, risk radar, and verified citations.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
