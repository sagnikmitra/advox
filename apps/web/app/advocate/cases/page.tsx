import Link from "next/link";

export default function AdvocateCasesPage() {
  return (
    <>
      {/* Sub-nav */}
      <div className="sticky top-[44px] z-40 border-b border-hairline bg-canvas-parchment/80 backdrop-blur-xl backdrop-saturate-[180%]">
        <div className="mx-auto flex h-[52px] max-w-content items-center justify-between px-6 md:px-10">
          <p className="text-tagline text-ink">Cases</p>
          <div className="flex items-center gap-4">
            <Link href="/advocate" className="text-btn-utility text-ink-muted-80 hover:text-primary">
              Workspace
            </Link>
            <Link href="/advocate/research" className="text-btn-utility text-ink-muted-80 hover:text-primary">
              Research
            </Link>
          </div>
        </div>
      </div>

      {/* Hero */}
      <section className="tile-light">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Case Workspaces.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Organize matters with risk mapping and document analysis.
          </p>
        </div>
      </section>

      {/* Cases list */}
      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content space-y-4">
          <Link href="/advocate/cases/demo-case" className="utility-card block text-left transition-colors hover:border-primary">
            <p className="text-body-strong text-ink">Demo Matter: Cheque Bounce - NI Act</p>
            <p className="mt-2 text-caption text-ink-muted-48">
              Jurisdiction: Delhi · Status: Active · Citation verification: pending
            </p>
          </Link>
        </div>
      </section>
    </>
  );
}
