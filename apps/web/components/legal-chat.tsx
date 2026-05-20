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
    <div className="utility-card">
      <p className="text-body-strong text-ink">
        {persona === "layman" ? "Legal Assistant" : "Advocate Assistant"}
      </p>
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <input
          value={state}
          onChange={(e) => setState(e.target.value)}
          className="input-rect"
          placeholder="State / jurisdiction"
        />
        <input
          value={incidentDate}
          onChange={(e) => setIncidentDate(e.target.value)}
          type="date"
          className="input-rect"
        />
      </div>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="mt-3 w-full rounded-lg border border-hairline bg-canvas px-4 py-3 text-body text-ink outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
        rows={5}
        placeholder="Describe legal situation, jurisdiction, dates, and documents"
      />
      <p className="mt-2 text-caption text-warning">{TRANSITION_WARNING}</p>
      <button
        onClick={handleRun}
        disabled={loading || message.trim().length < 5}
        className="btn-primary mt-4 disabled:opacity-50"
      >
        {loading ? "Running…" : "Run legal workflow"}
      </button>

      {route && (
        <p className="mt-4 text-caption text-ink-muted-48">
          Route: <span className="text-caption-strong text-ink">{route}</span>
        </p>
      )}
      {error && <p className="mt-3 text-caption text-error">{error}</p>}
      {response && (
        <pre className="mt-4 whitespace-pre-wrap rounded-lg border border-hairline bg-canvas-parchment p-5 text-caption text-ink-muted-80">
          {response}
        </pre>
      )}
    </div>
  );
}
