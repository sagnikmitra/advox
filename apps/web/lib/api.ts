import type { RouteResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export async function routeMessage(payload: Record<string, unknown>): Promise<RouteResponse> {
  const res = await fetch(`${API_BASE}/backend/api/ai/route`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error("Routing request failed");
  }
  return res.json();
}

export async function runScenario(payload: Record<string, unknown>): Promise<{ content: string; blocked: boolean }> {
  const res = await fetch(`${API_BASE}/backend/api/ai/scenario`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error("Scenario request failed");
  }
  return res.json();
}
