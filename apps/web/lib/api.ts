import type { RouteResponse } from "./types";
import { supabase } from "./supabase";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

async function getAuthHeaders(): Promise<Record<string, string>> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (supabase) {
    const { data } = await supabase.auth.getSession();
    if (data.session?.access_token) {
      headers["Authorization"] = `Bearer ${data.session.access_token}`;
    }
  }
  return headers;
}

export async function routeMessage(payload: Record<string, unknown>): Promise<RouteResponse> {
  const headers = await getAuthHeaders();
  const res = await fetch(`${API_BASE}/backend/api/ai/route`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error("Routing request failed");
  }
  return res.json();
}

export async function runScenario(payload: Record<string, unknown>): Promise<{ content: string; blocked: boolean }> {
  const headers = await getAuthHeaders();
  const res = await fetch(`${API_BASE}/backend/api/ai/scenario`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error("Scenario request failed");
  }
  return res.json();
}
