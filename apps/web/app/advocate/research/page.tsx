import { CitationPanel } from "@/components/citation-panel";
import { SourceViewer } from "@/components/source-viewer";

export default function ResearchPage() {
  return (
    <section className="page-shell grid gap-6 lg:grid-cols-3">
      <div className="space-y-4 lg:col-span-2">
        <h1 className="display-serif text-4xl">Precedent & Statute Research</h1>
        <div className="card">
          <textarea className="h-40 w-full rounded-md border border-hairline bg-canvas px-3 py-2 text-sm" placeholder="Search issue, act, section, forum, date" />
          <button className="mt-4 h-10 rounded-md bg-primary px-4 text-sm font-medium text-white">Run verified retrieval</button>
        </div>
        <SourceViewer />
      </div>
      <CitationPanel />
    </section>
  );
}
