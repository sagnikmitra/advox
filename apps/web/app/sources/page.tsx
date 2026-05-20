import { SourceViewer } from "@/components/source-viewer";
import { supabase } from "@/lib/supabase";

export default function SourcesPage() {
  const supabaseStatus = supabase ? "Configured" : "Not configured";
  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Public Legal Sources.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Only allowlisted, public, lawfully fetched and verified sources are available for citation.
          </p>
          <p className="mt-4 text-caption text-ink-muted-48">Supabase client: {supabaseStatus}</p>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content">
          <SourceViewer />
        </div>
      </section>
    </>
  );
}
