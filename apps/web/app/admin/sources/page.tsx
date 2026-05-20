export default function AdminSourcesPage() {
  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Source Verification.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Review source metadata, verification status, parser version, checksums, and citation eligibility.
          </p>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content">
          <div className="utility-card text-left">
            <p className="text-body-strong text-ink">Verification panel</p>
            <p className="mt-2 text-caption text-ink-muted-48">
              Source metadata, verification status, parser version, checksums, and citation eligibility.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
