export default function AdminIngestionPage() {
  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Ingestion Dashboard.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Monitor source ingestion pipeline status.
          </p>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content">
          <div className="utility-card text-left">
            <p className="text-body-strong text-ink">Pipeline stages</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {[
                "discovered", "fetched", "parsed", "normalized",
                "legally_classified", "citation_extracted", "verified",
                "embedded", "indexed", "available_for_rag"
              ].map((stage) => (
                <span key={stage} className="chip">{stage}</span>
              ))}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
