import { CitationPanel } from "@/components/citation-panel";
import { SourceViewer } from "@/components/source-viewer";
import Link from "next/link";

export default function ResearchPage() {
  return (
    <>
      {/* Sub-nav */}
      <div className="sticky top-[44px] z-40 border-b border-hairline bg-canvas-parchment/80 backdrop-blur-xl backdrop-saturate-[180%]">
        <div className="mx-auto flex h-[52px] max-w-content items-center justify-between px-6 md:px-10">
          <p className="text-tagline text-ink">Research</p>
          <div className="flex items-center gap-4">
            <Link href="/advocate" className="text-btn-utility text-ink-muted-80 hover:text-primary">
              Workspace
            </Link>
            <Link href="/advocate/cases" className="text-btn-utility text-ink-muted-80 hover:text-primary">
              Cases
            </Link>
          </div>
        </div>
      </div>

      {/* Hero */}
      <section className="tile-dark-2">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-on-dark">Precedent & Statute Research.</h1>
          <p className="mt-3 text-lead text-body-muted">
            Search issue, act, section, forum, and date with verified retrieval.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto grid max-w-grid gap-6 lg:grid-cols-3">
          <div className="space-y-6 lg:col-span-2">
            <div className="utility-card text-left">
              <textarea
                className="w-full rounded-lg border border-hairline bg-canvas-parchment px-4 py-3 text-body text-ink outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
                rows={5}
                placeholder="Search issue, act, section, forum, date"
              />
              <button className="btn-primary mt-4">Run verified retrieval</button>
            </div>
            <SourceViewer />
          </div>
          <CitationPanel />
        </div>
      </section>
    </>
  );
}
