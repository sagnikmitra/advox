"use client";

import { useState } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

type CaseResult = {
  cnr: string;
  status: string;
  case_type: string;
  case_number: string;
  court_name: string;
  petitioner: string;
  respondent: string;
  next_hearing: string;
  filing_date: string;
  decision_date: string;
  disposition: string;
  acts_sections: string[];
  case_history: { judge: string; hearing_date: string; purpose: string }[];
  error: string | null;
};

export default function CaseSearchPage() {
  const [cnr, setCnr] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CaseResult | null>(null);
  const [error, setError] = useState("");

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (cnr.trim().length < 16) {
      setError("CNR number must be at least 16 characters (e.g., WBBA020001232024)");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/backend/api/courts/case/search?cnr=${encodeURIComponent(cnr.trim())}`, {
        method: "POST",
      });
      const data = await res.json();
      if (data.error && data.error !== "captcha_required") {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch {
      setError("Failed to connect to case search service");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Case Search.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Look up case status by CNR number from the national eCourts database.
          </p>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-8 md:px-10">
        <div className="mx-auto max-w-[600px] space-y-6">
          {/* CNR Search */}
          <div className="utility-card">
            <p className="text-body-strong text-ink">Search by CNR Number</p>
            <p className="mt-1 text-caption text-ink-muted-48">
              The Case Number Record (CNR) is a unique 16-digit identifier assigned to every case filed in Indian courts.
            </p>
            <form onSubmit={handleSearch} className="mt-4 space-y-3">
              <input
                value={cnr}
                onChange={(e) => setCnr(e.target.value.toUpperCase())}
                className="input-rect w-full font-mono tracking-wide"
                placeholder="e.g. WBBA020001232024"
                maxLength={20}
              />
              <div className="flex items-center gap-3">
                <button type="submit" disabled={loading || cnr.trim().length < 16} className="btn-primary disabled:opacity-50">
                  {loading ? "Searching…" : "Search case"}
                </button>
                <p className="text-micro-legal text-ink-muted-48">
                  Format: 2 state + 2 district + 2 court + 2 year + serial
                </p>
              </div>
            </form>
            {error && <p className="mt-3 text-caption text-error">{error}</p>}
          </div>

          {/* CNR format guide */}
          <div className="utility-card text-left">
            <p className="text-body-strong text-ink">Understanding CNR Numbers</p>
            <div className="mt-3 overflow-x-auto">
              <table className="w-full text-caption">
                <thead>
                  <tr className="border-b border-hairline text-left text-micro-legal text-ink-muted-48">
                    <th className="pb-2 pr-4">Position</th>
                    <th className="pb-2 pr-4">Chars</th>
                    <th className="pb-2">Meaning</th>
                  </tr>
                </thead>
                <tbody className="text-ink-muted-80">
                  <tr className="border-b border-hairline/50"><td className="py-2 pr-4 font-mono">1-2</td><td className="py-2 pr-4">WB</td><td className="py-2">State code (West Bengal)</td></tr>
                  <tr className="border-b border-hairline/50"><td className="py-2 pr-4 font-mono">3-4</td><td className="py-2 pr-4">BA</td><td className="py-2">District code</td></tr>
                  <tr className="border-b border-hairline/50"><td className="py-2 pr-4 font-mono">5-6</td><td className="py-2 pr-4">02</td><td className="py-2">Court complex code</td></tr>
                  <tr className="border-b border-hairline/50"><td className="py-2 pr-4 font-mono">7-8</td><td className="py-2 pr-4">00</td><td className="py-2">Year prefix</td></tr>
                  <tr><td className="py-2 pr-4 font-mono">9-16</td><td className="py-2 pr-4">01232024</td><td className="py-2">Serial / registration</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Result */}
          {result && (
            <div className="utility-card text-left space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-body-strong text-ink">Case Details</p>
                  <p className="text-micro-legal text-ink-muted-48 font-mono">{result.cnr}</p>
                </div>
                <span className={`rounded-pill px-3 py-1 text-micro-legal ${
                  result.status === "captcha_required"
                    ? "bg-warning/10 text-warning"
                    : result.error
                    ? "bg-error/10 text-error"
                    : "bg-[#34C759]/10 text-[#34C759]"
                }`}>
                  {result.status === "captcha_required" ? "CAPTCHA Required" : result.status || "Retrieved"}
                </span>
              </div>

              {result.status === "captcha_required" && (
                <div className="rounded-lg border border-warning/30 bg-warning/5 p-4">
                  <p className="text-caption text-ink">
                    eCourts requires CAPTCHA verification for case lookups. This is a security measure by the Indian judiciary.
                  </p>
                  <p className="mt-2 text-caption text-ink-muted-48">
                    You can search directly on{" "}
                    <a href="https://services.ecourts.gov.in/ecourtindia_v6/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                      eCourts India
                    </a>{" "}
                    using this CNR number.
                  </p>
                </div>
              )}

              {result.case_type && (
                <div className="grid gap-3 md:grid-cols-2">
                  {result.case_type && <div><p className="text-micro-legal text-ink-muted-48">Case Type</p><p className="text-caption text-ink">{result.case_type}</p></div>}
                  {result.case_number && <div><p className="text-micro-legal text-ink-muted-48">Case Number</p><p className="text-caption text-ink">{result.case_number}</p></div>}
                  {result.court_name && <div><p className="text-micro-legal text-ink-muted-48">Court</p><p className="text-caption text-ink">{result.court_name}</p></div>}
                  {result.filing_date && <div><p className="text-micro-legal text-ink-muted-48">Filing Date</p><p className="text-caption text-ink">{result.filing_date}</p></div>}
                  {result.next_hearing && <div><p className="text-micro-legal text-ink-muted-48">Next Hearing</p><p className="text-caption text-ink font-semibold">{result.next_hearing}</p></div>}
                  {result.decision_date && <div><p className="text-micro-legal text-ink-muted-48">Decision Date</p><p className="text-caption text-ink">{result.decision_date}</p></div>}
                </div>
              )}

              {result.petitioner && (
                <div className="border-t border-hairline pt-3">
                  <div className="grid gap-3 md:grid-cols-2">
                    <div><p className="text-micro-legal text-ink-muted-48">Petitioner</p><p className="text-caption text-ink">{result.petitioner}</p></div>
                    <div><p className="text-micro-legal text-ink-muted-48">Respondent</p><p className="text-caption text-ink">{result.respondent}</p></div>
                  </div>
                </div>
              )}

              {result.acts_sections.length > 0 && (
                <div className="border-t border-hairline pt-3">
                  <p className="text-micro-legal text-ink-muted-48">Acts & Sections</p>
                  <div className="mt-1 flex flex-wrap gap-2">
                    {result.acts_sections.map((act, i) => (
                      <span key={i} className="rounded-pill bg-ink/5 px-2 py-0.5 text-micro-legal text-ink-muted-80">{act}</span>
                    ))}
                  </div>
                </div>
              )}

              {result.case_history.length > 0 && (
                <div className="border-t border-hairline pt-3">
                  <p className="text-micro-legal text-ink-muted-48 mb-2">Case History</p>
                  <div className="space-y-1">
                    {result.case_history.map((h, i) => (
                      <div key={i} className="flex gap-3 text-micro-legal text-ink-muted-80">
                        <span className="shrink-0 font-mono">{h.hearing_date}</span>
                        <span>{h.purpose}</span>
                        {h.judge && <span className="text-ink-muted-48">({h.judge})</span>}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Quick links */}
          <div className="utility-card text-left">
            <p className="text-body-strong text-ink">Direct court portals</p>
            <div className="mt-3 grid gap-2 md:grid-cols-2">
              <a href="https://services.ecourts.gov.in/ecourtindia_v6/" target="_blank" rel="noopener noreferrer" className="text-caption text-primary hover:underline">eCourts District Courts &rarr;</a>
              <a href="https://hcservices.ecourts.gov.in/hcservices/" target="_blank" rel="noopener noreferrer" className="text-caption text-primary hover:underline">eCourts High Courts &rarr;</a>
              <a href="https://main.sci.gov.in/case-status" target="_blank" rel="noopener noreferrer" className="text-caption text-primary hover:underline">Supreme Court Case Status &rarr;</a>
              <a href="https://njdg.ecourts.gov.in/" target="_blank" rel="noopener noreferrer" className="text-caption text-primary hover:underline">National Judicial Data Grid &rarr;</a>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
