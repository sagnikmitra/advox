import { SourcesList } from "@/components/sources-list";

export default function SourcesPage() {
  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Public Legal Sources.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Only allowlisted, public, lawfully fetched and verified sources are available for citation.
          </p>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-grid">
          <SourcesList />
        </div>
      </section>
    </>
  );
}
