"use client";

import { useEffect, useState } from "react";
import { supabase, type LegalSource } from "@/lib/supabase";

export default function AdminSourcesPage() {
  const [sources, setSources] = useState<LegalSource[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!supabase) return;
    supabase
      .from("legal_sources")
      .select("*")
      .order("created_at", { ascending: false })
      .limit(50)
      .then(({ data }) => {
        if (data) setSources(data as LegalSource[]);
        setLoading(false);
      });
  }, []);

  const pending = sources.filter((s) => s.verification_status === "pending_review");
  const verified = sources.filter((s) => s.verification_status === "verified");

  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Source Verification.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            {sources.length} total · {verified.length} verified · {pending.length} pending review
          </p>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content space-y-6">
          {loading ? (
            <p className="text-caption text-ink-muted-48">Loading…</p>
          ) : (
            <>
              {pending.length > 0 && (
                <div>
                  <p className="text-body-strong text-ink">Pending Review ({pending.length})</p>
                  <div className="mt-3 space-y-2">
                    {pending.map((s) => (
                      <div key={s.id} className="utility-card text-left">
                        <p className="text-caption-strong text-ink">{s.title}</p>
                        <div className="mt-1 flex flex-wrap gap-3 text-micro-legal text-ink-muted-48">
                          <span>{s.source_type}</span>
                          <span>{s.authority_level}</span>
                          {s.source_domain && <span>{s.source_domain}</span>}
                          <span className="text-warning">{s.verification_status}</span>
                          <span>{s.index_status}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div>
                <p className="text-body-strong text-ink">All Sources ({sources.length})</p>
                <div className="mt-3 space-y-2">
                  {sources.map((s) => (
                    <div key={s.id} className="utility-card text-left">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="text-caption-strong text-ink">{s.title}</p>
                          <div className="mt-1 flex flex-wrap gap-3 text-micro-legal text-ink-muted-48">
                            <span>{s.source_type}</span>
                            <span>{s.authority_level}</span>
                            {s.source_domain && <span>{s.source_domain}</span>}
                          </div>
                        </div>
                        <div className="flex gap-2 text-micro-legal">
                          <span className={s.verification_status === "verified" ? "text-success" : "text-warning"}>
                            {s.verification_status}
                          </span>
                          <span className={s.index_status === "indexed" ? "text-success" : "text-ink-muted-48"}>
                            {s.index_status}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </section>
    </>
  );
}
