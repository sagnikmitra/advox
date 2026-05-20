import Link from "next/link";

export default function AdvocateCasesPage() {
  return (
    <section className="page-shell space-y-4">
      <h1 className="display-serif text-4xl">Case Workspaces</h1>
      <div className="grid gap-4">
        <Link href="/advocate/cases/demo-case" className="card block">
          <h2 className="text-lg font-medium">Demo Matter: Cheque Bounce - NI Act</h2>
          <p className="mt-1 text-sm text-body">Jurisdiction: Delhi · Status: Active · Citation verification: pending</p>
        </Link>
      </div>
    </section>
  );
}
