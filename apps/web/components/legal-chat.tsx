"use client";

import { useState } from "react";

import { runScenario, routeMessage } from "@/lib/api";
import { TRANSITION_WARNING } from "@/lib/constants";

export function LegalChat({ persona }: { persona: "layman" | "advocate" }) {
  const [message, setMessage] = useState("");
  const [state, setState] = useState("");
  const [incidentDate, setIncidentDate] = useState("");
  const [route, setRoute] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleRun() {
    setLoading(true);
    setError("");
    setResponse("");
    setRoute("");

    try {
      const payload = {
        message,
        persona,
        language: "en",
        state: state || null,
        incident_date: incidentDate || null,
        documents: []
      };

      const routing = await routeMessage(payload);
      setRoute(routing.route);

      const scenario = await runScenario(payload);
      setResponse(scenario.content);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h3 className="text-lg font-medium">{persona === "layman" ? "Layman Legal Assistant" : "Advocate Legal Assistant"}</h3>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        <input
          value={state}
          onChange={(e) => setState(e.target.value)}
          className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm"
          placeholder="State / jurisdiction"
        />
        <input
          value={incidentDate}
          onChange={(e) => setIncidentDate(e.target.value)}
          type="date"
          className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm"
        />
      </div>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="mt-3 h-36 w-full rounded-md border border-hairline bg-canvas px-3 py-2 text-sm"
        placeholder="Describe legal situation, jurisdiction, dates, and documents"
      />
      <p className="mt-2 text-xs text-warning">{TRANSITION_WARNING}</p>
      <button
        onClick={handleRun}
        disabled={loading || message.trim().length < 5}
        className="mt-4 h-10 rounded-md bg-primary px-4 text-sm font-medium text-white disabled:opacity-60"
      >
        {loading ? "Running..." : "Run legal workflow"}
      </button>

      {route && <p className="mt-3 text-xs uppercase tracking-wide text-muted">route: {route}</p>}
      {error && <p className="mt-2 text-sm text-error">{error}</p>}
      {response && <pre className="mt-3 whitespace-pre-wrap rounded-md border border-hairline bg-canvas p-3 text-sm text-body">{response}</pre>}
    </div>
  );
}
