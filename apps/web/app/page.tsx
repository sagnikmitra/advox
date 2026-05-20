import Link from "next/link";
import { PersonaSelector } from "@/components/persona-selector";

export default function HomePage() {
  return (
    <>
      {/* Hero tile — white */}
      <section className="tile-light flex flex-col items-center">
        <p className="text-caption text-primary">Indian law only · verified-source first</p>
        <h1 className="headline-tight mt-4 max-w-3xl text-hero-display text-ink max-md:text-display-lg">
          Legal intelligence for India.
        </h1>
        <p className="mt-4 max-w-2xl text-lead text-ink-muted-80">
          Persona-aware guidance for citizens and advocates. Citation gating blocks unsafe output when verification fails.
        </p>
        <div className="mt-8 flex gap-3">
          <Link href="/ask" className="btn-primary">Get started</Link>
          <Link href="/advocate" className="btn-secondary">For advocates</Link>
        </div>
      </section>

      {/* Persona selector — parchment */}
      <section className="tile-parchment">
        <div className="mx-auto max-w-content">
          <h2 className="headline-tight text-display-lg text-ink">Choose your path.</h2>
          <p className="mt-3 text-lead text-ink-muted-80">Two modes, one verified knowledge base.</p>
          <div className="mt-12">
            <PersonaSelector />
          </div>
        </div>
      </section>

      {/* Features — dark tile */}
      <section className="tile-dark">
        <div className="mx-auto max-w-content">
          <h2 className="headline-tight text-display-lg text-on-dark">Built to fail closed.</h2>
          <p className="mt-3 text-lead text-body-muted">
            Every response is citation-gated. If verification fails, the system blocks output rather than hallucinate.
          </p>
          <div className="mt-12 grid gap-6 text-left md:grid-cols-3">
            <div>
              <p className="text-tagline text-on-dark">Citation Gating</p>
              <p className="mt-2 text-body text-body-muted">
                Responses require verified source backing. Unverified claims are blocked, not softened.
              </p>
            </div>
            <div>
              <p className="text-tagline text-on-dark">BNS/IPC Aware</p>
              <p className="mt-2 text-body text-body-muted">
                Automatic statute transition detection based on incident date — before or after 1 July 2024.
              </p>
            </div>
            <div>
              <p className="text-tagline text-on-dark">Risk Radar</p>
              <p className="mt-2 text-body text-body-muted">
                Missed deadlines, jurisdiction defects, limitation risk, and procedural non-compliance — surfaced upfront.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Tools — white tile */}
      <section className="tile-light">
        <div className="mx-auto max-w-content">
          <h2 className="headline-tight text-display-lg text-ink">Advocate toolkit.</h2>
          <p className="mt-3 text-lead text-ink-muted-80">
            Research, case prep, and procedural mapping — all citation-backed.
          </p>
          <div className="mt-12 grid gap-5 md:grid-cols-3">
            <Link href="/advocate/research" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">Precedent Research</p>
              <p className="mt-2 text-caption text-ink-muted-48">Search statutes, sections, and case law with verified retrieval.</p>
            </Link>
            <Link href="/advocate/cases" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">Case Workspaces</p>
              <p className="mt-2 text-caption text-ink-muted-48">Organize matters with risk mapping and document analysis.</p>
            </Link>
            <Link href="/upload" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">Document Analyzer</p>
              <p className="mt-2 text-caption text-ink-muted-48">Upload legal documents for summary, deadlines, and citation extraction.</p>
            </Link>
          </div>
        </div>
      </section>

      {/* Sources — dark tile 2 */}
      <section className="tile-dark-2">
        <div className="mx-auto max-w-content">
          <h2 className="headline-tight text-display-lg text-on-dark">Verified sources only.</h2>
          <p className="mt-3 text-lead text-body-muted">
            Only allowlisted, public, lawfully fetched sources enter the knowledge base. Every citation links back.
          </p>
          <div className="mt-8">
            <Link href="/sources" className="btn-primary">Browse sources</Link>
          </div>
        </div>
      </section>
    </>
  );
}
