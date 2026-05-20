export default function PrivacyPage() {
  return (
    <section className="page-shell space-y-4">
      <h1 className="display-serif text-4xl">Privacy Policy</h1>
      <div className="card space-y-2 text-sm text-body">
        <p>Default retention is minimal. Uploaded documents use TTL deletion unless workspace save is explicitly enabled.</p>
        <p>PII scrubbing runs before model calls. Raw sensitive prompts are not persisted by default.</p>
        <p>Tenant isolation and role-based access control are required for production deployment.</p>
      </div>
    </section>
  );
}
