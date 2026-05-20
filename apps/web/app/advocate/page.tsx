import { AdvocateWorkspace } from "@/components/advocate-workspace";
import { LegalChat } from "@/components/legal-chat";

export default function AdvocatePage() {
  return (
    <section className="page-shell space-y-6">
      <h1 className="display-serif text-4xl">Advocate Workspace</h1>
      <div className="grid gap-3 md:grid-cols-5">
        <input className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm" placeholder="Court" />
        <input className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm" placeholder="Matter type" />
        <input className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm" placeholder="Jurisdiction" />
        <input type="date" className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm" />
        <button className="h-10 rounded-md bg-primary text-sm font-medium text-white">Create case workspace</button>
      </div>
      <LegalChat persona="advocate" />
      <AdvocateWorkspace />
    </section>
  );
}
