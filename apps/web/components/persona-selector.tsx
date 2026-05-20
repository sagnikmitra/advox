import Link from "next/link";

export function PersonaSelector() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Link href="/ask" className="group rounded-lg bg-canvas p-10 text-left shadow-product transition-transform hover:scale-[1.01]">
        <p className="text-tagline text-ink">For Common People</p>
        <p className="mt-3 text-body text-ink-muted-80">
          Simple legal procedure guidance, safety-first steps, and document checklists.
        </p>
        <span className="mt-6 inline-block text-body text-primary group-hover:underline">Get started →</span>
      </Link>
      <Link href="/advocate" className="group rounded-lg bg-surface-tile-1 p-10 text-left transition-transform hover:scale-[1.01]">
        <p className="text-tagline text-on-dark">For Advocates</p>
        <p className="mt-3 text-body text-body-muted">
          Citation-backed research workflows, case prep, procedural and risk mapping.
        </p>
        <span className="mt-6 inline-block text-body text-primary-on-dark group-hover:underline">Open workspace →</span>
      </Link>
    </div>
  );
}
