"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import Link from "next/link";
import { supabase } from "@/lib/supabase";

type Court = {
  id: string;
  name: string;
  short_name: string | null;
  court_type: string;
  state_code: string | null;
  state_name: string | null;
  district_name: string | null;
  bench: string | null;
  website: string | null;
};

const TYPE_LABELS: Record<string, string> = {
  supreme_court: "Supreme Court",
  high_court: "High Court",
  district_court: "District Court",
  sessions_court: "Sessions Court",
  tribunal: "Tribunal",
};

const TYPE_COLORS: Record<string, string> = {
  supreme_court: "bg-primary/10 text-primary",
  high_court: "bg-[#5856D6]/10 text-[#5856D6]",
  district_court: "bg-[#34C759]/10 text-[#34C759]",
};

function CourtsContent() {
  const searchParams = useSearchParams();
  const [courts, setCourts] = useState<Court[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState(searchParams.get("type") || "all");
  const [stateFilter, setStateFilter] = useState("");
  const [states, setStates] = useState<{ state_code: string; state_name: string }[]>([]);

  useEffect(() => {
    if (!supabase) return;
    supabase
      .from("courts")
      .select("state_code, state_name")
      .not("state_code", "is", null)
      .then(({ data }) => {
        if (data) {
          const unique = Array.from(new Map(data.map((d) => [d.state_code, d])).values())
            .sort((a, b) => (a.state_name || "").localeCompare(b.state_name || ""));
          setStates(unique);
        }
      });
  }, []);

  useEffect(() => {
    if (!supabase) {
      setLoading(false);
      return;
    }

    let query = supabase
      .from("courts")
      .select("id, name, short_name, court_type, state_code, state_name, district_name, bench, website")
      .order("court_type")
      .order("state_name")
      .order("district_name")
      .limit(200);

    if (typeFilter && typeFilter !== "all") {
      query = query.eq("court_type", typeFilter);
    }
    if (stateFilter) {
      query = query.eq("state_code", stateFilter);
    }
    if (search) {
      query = query.or(`name.ilike.%${search}%,district_name.ilike.%${search}%,state_name.ilike.%${search}%`);
    }

    query.then(({ data }) => {
      setCourts((data as Court[]) || []);
      setLoading(false);
    });
  }, [typeFilter, stateFilter, search]);

  const grouped = courts.reduce<Record<string, Court[]>>((acc, court) => {
    const key = court.court_type;
    if (!acc[key]) acc[key] = [];
    acc[key].push(court);
    return acc;
  }, {});

  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Courts of India.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Complete directory of Indian courts — Supreme Court, 25 High Courts, and district courts across every state.
          </p>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-8 md:px-10">
        <div className="mx-auto max-w-grid">
          {/* Filters */}
          <div className="flex flex-wrap gap-3">
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search courts…"
              className="input-rect flex-1 min-w-[200px]"
            />
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="input-rect"
            >
              <option value="all">All types</option>
              <option value="supreme_court">Supreme Court</option>
              <option value="high_court">High Courts</option>
              <option value="district_court">District Courts</option>
            </select>
            <select
              value={stateFilter}
              onChange={(e) => setStateFilter(e.target.value)}
              className="input-rect"
            >
              <option value="">All states</option>
              {states.map((s) => (
                <option key={s.state_code} value={s.state_code}>{s.state_name}</option>
              ))}
            </select>
          </div>

          <p className="mt-4 text-caption text-ink-muted-48">
            {courts.length} court{courts.length !== 1 ? "s" : ""} found
          </p>

          {loading ? (
            <p className="mt-8 text-center text-caption text-ink-muted-48">Loading courts…</p>
          ) : (
            <div className="mt-6 space-y-10">
              {Object.entries(grouped).map(([type, items]) => (
                <div key={type}>
                  <div className="flex items-center gap-3">
                    <h2 className="text-body-strong text-ink">{TYPE_LABELS[type] || type}</h2>
                    <span className="text-caption text-ink-muted-48">{items.length}</span>
                  </div>
                  <div className="mt-3 grid gap-3 md:grid-cols-2 lg:grid-cols-3">
                    {items.map((court) => (
                      <div key={court.id} className="utility-card text-left">
                        <div className="flex items-start justify-between gap-2">
                          <p className="text-caption-strong text-ink">{court.name}</p>
                          <span className={`shrink-0 rounded-pill px-2 py-0.5 text-micro-legal ${TYPE_COLORS[court.court_type] || "bg-ink/5 text-ink-muted-48"}`}>
                            {TYPE_LABELS[court.court_type]?.split(" ")[0] || court.court_type}
                          </span>
                        </div>
                        <div className="mt-2 flex flex-wrap gap-2 text-micro-legal text-ink-muted-48">
                          {court.state_name && <span>{court.state_name}</span>}
                          {court.district_name && <span>· {court.district_name}</span>}
                          {court.bench && <span>· Bench: {court.bench}</span>}
                        </div>
                        {court.website && (
                          <a
                            href={court.website}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-2 inline-block text-micro-legal text-primary hover:underline"
                          >
                            Official website &rarr;
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
              {courts.length === 0 && (
                <p className="py-12 text-center text-caption text-ink-muted-48">No courts match your search.</p>
              )}
            </div>
          )}
        </div>
      </section>
    </>
  );
}

export default function CourtsPage() {
  return (
    <Suspense fallback={<section className="tile-parchment"><p className="text-caption text-ink-muted-48">Loading…</p></section>}>
      <CourtsContent />
    </Suspense>
  );
}
