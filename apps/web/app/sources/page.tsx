import { SourceViewer } from "@/components/source-viewer";
import { supabase } from "@/lib/supabase";

export default function SourcesPage() {
  const supabaseStatus = supabase ? "Configured" : "Not configured";
  return (
    <section className="page-shell space-y-4">
      <h1 className="display-serif text-4xl">Public Legal Source Browser</h1>
      <p className="text-sm text-body">Only allowlisted, public, lawfully fetched and verified sources are available for citation.</p>
      <p className="text-xs uppercase tracking-wide text-muted">Supabase client: {supabaseStatus}</p>
      <SourceViewer />
    </section>
  );
}
