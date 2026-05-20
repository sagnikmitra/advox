import { DocumentUpload } from "@/components/document-upload";

export default function UploadPage() {
  return (
    <section className="page-shell space-y-4">
      <h1 className="display-serif text-4xl">Document Analyzer</h1>
      <DocumentUpload />
      <div className="card text-sm text-body">
        Output format includes summary, procedural history, deadlines, risk radar, and verified citations.
      </div>
    </section>
  );
}
