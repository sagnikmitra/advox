export default function PrivacyPage() {
  return (
    <>
      <section className="tile-light">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Privacy Policy.</h1>
        </div>
      </section>

      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content">
          <div className="utility-card space-y-4 text-left">
            <p className="text-body text-ink-muted-80">
              Default retention is minimal. Uploaded documents use TTL deletion unless workspace save is explicitly enabled.
            </p>
            <p className="text-body text-ink-muted-80">
              PII scrubbing runs before model calls. Raw sensitive prompts are not persisted by default.
            </p>
            <p className="text-body text-ink-muted-80">
              Tenant isolation and role-based access control are required for production deployment.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
