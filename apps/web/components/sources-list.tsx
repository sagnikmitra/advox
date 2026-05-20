"use client";

import { useEffect, useState } from "react";
import { supabase, type LegalSource, type IngestionSource } from "@/lib/supabase";

const AUTHORITY_ORDER: Record<string, number> = {
  constitution: 0,
  supreme_court: 1,
  central_statute: 2,
  high_court: 3,
  state_statute: 4,
  district_court: 5,
  tribunal: 6,
  ministry: 7,
  gazette: 8,
  secondary: 9,
};

const STATUS_COLORS: Record<string, string> = {
  verified: "text-success",
  pending_review: "text-warning",
  unverified: "text-ink-muted-48",
  rejected: "text-error",
};

const INDEX_COLORS: Record<string, string> = {
  indexed: "text-success",
  queued: "text-warning",
  not_indexed: "text-ink-muted-48",
  failed: "text-error",
};

export function SourcesList() {
  const [sources, setSources] = useState<LegalSource[]>([]);
  const [ingestionSources, setIngestionSources] = useState<IngestionSource[]>([]);
  const [filter, setFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!supabase) {
      setError("Supabase not configured");
      setLoading(false);
      return;
    }

    async function load() {
      const [sourcesRes, ingestionRes] = await Promise.all([
        supabase!.from("legal_sources").select("*").order("authority_level").limit(100),
        supabase!.from("ingestion_sources").select("*").order("name"),
      ]);

      if (sourcesRes.error) {
        setError(sourcesRes.error.message);
      } else {
        const sorted = (sourcesRes.data as LegalSource[]).sort(
          (a, b) => (AUTHORITY_ORDER[a.authority_level] ?? 99) - (AUTHORITY_ORDER[b.authority_level] ?? 99)
        );
        setSources(sorted);
      }

      if (!ingestionRes.error && ingestionRes.data) {
        const unique = (ingestionRes.data as IngestionSource[]).filter(
          (v, i, a) => a.findIndex((t) => t.name === v.name) === i
        );
        setIngestionSources(unique);
      }

      setLoading(false);
    }

    load();
  }, []);

  const filtered = filter === "all" ? sources : sources.filter((s) => s.verification_status === filter);

  if (loading) {
    return <p className="text-caption text-ink-muted-48">Loading sources…</p>;
  }

  if (error) {
    return <p className="text-caption text-error">{error}</p>;
  }

  return (
    <div className="space-y-10">
      {/* Ingestion Registry */}
      <div>
        <p className="text-body-strong text-ink">Source Registry</p>
        <p className="mt-1 text-caption text-ink-muted-48">
          {ingestionSources.length} registered sources across statutory, judgment, tribunal, and citizen service categories.
        </p>
        <div className="mt-4 grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {ingestionSources.map((src) => (
            <div key={src.id} className="utility-card text-left">
              <div className="flex items-start justify-between">
                <p className="text-caption-strong text-ink">{src.name}</p>
                {src.is_official && (
                  <span className="rounded-pill bg-primary/10 px-2 py-0.5 text-micro-legal text-primary">Official</span>
                )}
              </div>
              <p className="mt-1 text-micro-legal text-ink-muted-48">{src.base_domain}</p>
              <div className="mt-2 flex gap-2">
                <span className="text-micro-legal text-ink-muted-48">{src.source_category}</span>
                {src.requires_captcha && (
                  <span className="text-micro-legal text-warning">CAPTCHA</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Legal Sources */}
      <div>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-body-strong text-ink">Verified Legal Sources</p>
            <p className="mt-1 text-caption text-ink-muted-48">
              {sources.length} sources · {sources.filter((s) => s.verification_status === "verified").length} verified · {sources.filter((s) => s.index_status === "indexed").length} indexed
            </p>
          </div>
          <div className="flex gap-2">
            {["all", "verified", "pending_review", "unverified"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={filter === f ? "chip-selected" : "chip"}
              >
                {f === "all" ? "All" : f.replace("_", " ")}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-4 space-y-2">
          {filtered.map((source) => (
            <div key={source.id} className="utility-card text-left">
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div className="min-w-0 flex-1">
                  <p className="text-caption-strong text-ink truncate">{source.title}</p>
                  <div className="mt-1 flex flex-wrap gap-3 text-micro-legal">
                    <span className="text-ink-muted-48">{source.source_type}</span>
                    <span className="text-ink-muted-48">{source.authority_level.replace("_", " ")}</span>
                    {source.source_domain && (
                      <span className="text-ink-muted-48">{source.source_domain}</span>
                    )}
                    {source.jurisdiction_state && (
                      <span className="text-ink-muted-48">{source.jurisdiction_state}</span>
                    )}
                  </div>
                </div>
                <div className="flex gap-3 text-micro-legal">
                  <span className={STATUS_COLORS[source.verification_status] ?? "text-ink-muted-48"}>
                    {source.verification_status}
                  </span>
                  <span className={INDEX_COLORS[source.index_status] ?? "text-ink-muted-48"}>
                    {source.index_status}
                  </span>
                </div>
              </div>
            </div>
          ))}
          {filtered.length === 0 && (
            <p className="py-8 text-center text-caption text-ink-muted-48">No sources match this filter.</p>
          )}
        </div>
      </div>
    </div>
  );
}
