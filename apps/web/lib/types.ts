export type Persona = "layman" | "advocate";

export type CitationStatus =
  | "verified"
  | "partially_verified"
  | "unverified"
  | "conflicting"
  | "missing";

export type RouteResponse = {
  route:
    | "scenario_mapping"
    | "document_analysis"
    | "precedent_research"
    | "statute_lookup"
    | "procedural_guidance"
    | "translation"
    | "advocate_handoff"
    | "refusal";
  persona: Persona;
  language: string;
  jurisdiction_state: string | null;
  legal_domain: string;
  urgency: "low" | "medium" | "high" | "emergency";
  requires_verified_sources: boolean;
  requires_citation_verification: boolean;
  requires_human_lawyer: boolean;
  missing_critical_fields: string[];
};
