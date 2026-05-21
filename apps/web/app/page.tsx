import Link from "next/link";
import { PersonaSelector } from "@/components/persona-selector";

export default function HomePage() {
  return (
    <>
      {/* Hero */}
      <section className="tile-light flex flex-col items-center">
        <p className="text-caption text-primary">Indian law only · verified-source first · 95+ courts indexed</p>
        <h1 className="headline-tight mt-4 max-w-3xl text-hero-display text-ink max-md:text-display-lg">
          Legal intelligence for India.
        </h1>
        <p className="mt-4 max-w-2xl text-lead text-ink-muted-80">
          Navigate Indian law with confidence. AI-powered guidance for citizens, case tracking for advocates,
          and a verified knowledge base covering BNS, BNSS, BSA, and the Constitution.
        </p>
        <div className="mt-8 flex gap-3">
          <Link href="/ask" className="btn-primary">Get started free</Link>
          <Link href="/courts" className="btn-secondary">Browse courts</Link>
        </div>
      </section>

      {/* Stats bar */}
      <section className="bg-surface-black px-6 py-8 md:px-10">
        <div className="mx-auto grid max-w-content grid-cols-2 gap-6 text-center md:grid-cols-4">
          <div>
            <p className="font-display text-[32px] font-semibold tracking-tight text-on-dark">25</p>
            <p className="text-caption text-body-muted">High Courts</p>
          </div>
          <div>
            <p className="font-display text-[32px] font-semibold tracking-tight text-on-dark">69+</p>
            <p className="text-caption text-body-muted">District Courts</p>
          </div>
          <div>
            <p className="font-display text-[32px] font-semibold tracking-tight text-on-dark">42</p>
            <p className="text-caption text-body-muted">Verified Legal Chunks</p>
          </div>
          <div>
            <p className="font-display text-[32px] font-semibold tracking-tight text-on-dark">3</p>
            <p className="text-caption text-body-muted">AI Models with Fallback</p>
          </div>
        </div>
      </section>

      {/* Persona selector */}
      <section className="tile-parchment">
        <div className="mx-auto max-w-content">
          <h2 className="headline-tight text-display-lg text-ink">Choose your path.</h2>
          <p className="mt-3 text-lead text-ink-muted-80">Two modes, one verified knowledge base.</p>
          <div className="mt-12">
            <PersonaSelector />
          </div>
        </div>
      </section>

      {/* Core features */}
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
              <p className="text-tagline text-on-dark">BNS / IPC Aware</p>
              <p className="mt-2 text-body text-body-muted">
                Automatic statute transition detection based on incident date — before or after 1 July 2024.
              </p>
            </div>
            <div>
              <p className="text-tagline text-on-dark">Case Tracker</p>
              <p className="mt-2 text-body text-body-muted">
                Search case status by CNR number across district courts, high courts, and the Supreme Court.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Courts directory preview */}
      <section className="tile-light">
        <div className="mx-auto max-w-content">
          <h2 className="headline-tight text-display-lg text-ink">Every court. One directory.</h2>
          <p className="mt-3 text-lead text-ink-muted-80">
            Supreme Court, 25 High Courts, and district courts across India — searchable, with eCourts integration.
          </p>
          <div className="mt-12 grid gap-5 md:grid-cols-3">
            <Link href="/courts?type=supreme_court" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">Supreme Court of India</p>
              <p className="mt-2 text-caption text-ink-muted-48">Apex court with original and appellate jurisdiction across all legal matters.</p>
            </Link>
            <Link href="/courts?type=high_court" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">High Courts</p>
              <p className="mt-2 text-caption text-ink-muted-48">25 High Courts covering every state and union territory. Writ jurisdiction under Article 226.</p>
            </Link>
            <Link href="/courts?type=district_court" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">District Courts</p>
              <p className="mt-2 text-caption text-ink-muted-48">District & Sessions Courts across India. Starting with West Bengal and major cities.</p>
            </Link>
          </div>
        </div>
      </section>

      {/* Advocate toolkit */}
      <section className="tile-parchment">
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
            <Link href="/case-search" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">Case Search</p>
              <p className="mt-2 text-caption text-ink-muted-48">Look up case status by CNR number from the national eCourts database.</p>
            </Link>
            <Link href="/upload" className="utility-card text-left transition-colors hover:border-primary">
              <p className="text-body-strong text-ink">Document Analyzer</p>
              <p className="mt-2 text-caption text-ink-muted-48">Upload legal documents for summary, deadlines, and citation extraction.</p>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="tile-dark-2">
        <div className="mx-auto max-w-content">
          <h2 className="headline-tight text-display-lg text-on-dark">Verified sources only.</h2>
          <p className="mt-3 text-lead text-body-muted">
            Only allowlisted, public, lawfully fetched sources enter the knowledge base. Every citation links back.
          </p>
          <div className="mt-8 flex gap-3 justify-center">
            <Link href="/sources" className="btn-primary">Browse sources</Link>
            <Link href="/signup" className="btn-secondary !border-on-dark/30 !text-on-dark">Create free account</Link>
          </div>
        </div>
      </section>
    </>
  );
}
