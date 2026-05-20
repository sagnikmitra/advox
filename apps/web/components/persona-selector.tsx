import Link from "next/link";

export function PersonaSelector() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Link href="/ask" className="card hover:border-primary">
        <h2 className="display-serif text-3xl text-ink">For Common People</h2>
        <p className="mt-3 text-body">Simple legal procedure guidance, safety-first steps, and document checklists.</p>
      </Link>
      <Link href="/advocate" className="dark-card hover:bg-surface-dark-elevated">
        <h2 className="display-serif text-3xl">For Advocates</h2>
        <p className="mt-3 text-[#d8d4ce]">Citation-backed research workflows, case prep, procedural and risk mapping.</p>
      </Link>
    </div>
  );
}
