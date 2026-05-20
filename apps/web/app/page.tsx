import { PersonaSelector } from "@/components/persona-selector";

export default function HomePage() {
  return (
    <section className="page-shell space-y-8 py-20">
      <p className="text-xs uppercase tracking-[1.5px] text-muted">Indian law only · verified-source first</p>
      <h1 className="display-serif max-w-4xl text-5xl leading-tight text-ink md:text-7xl">
        Legal information and procedure workflows for India, built to fail closed.
      </h1>
      <p className="max-w-3xl text-lg text-body">
        Persona-aware guidance for citizens and advocates. Citation gating blocks unsafe legal output when verification fails.
      </p>
      <PersonaSelector />
    </section>
  );
}
