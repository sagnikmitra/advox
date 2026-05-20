import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;

export const supabase =
  supabaseUrl && supabaseKey
    ? createClient(supabaseUrl, supabaseKey)
    : null;

export type LegalSource = {
  id: string;
  title: string;
  source_type: string;
  authority_level: string;
  verification_status: string;
  index_status: string;
  source_url: string | null;
  source_domain: string | null;
  act_name: string | null;
  section_number: string | null;
  court_name: string | null;
  jurisdiction_state: string | null;
  language: string;
  created_at: string;
};

export type IngestionSource = {
  id: string;
  name: string;
  source_category: string;
  base_domain: string;
  is_official: boolean;
  is_active: boolean;
  requires_captcha: boolean;
  requires_login: boolean;
  notes: string | null;
};

export type GlossaryTerm = {
  id: string;
  canonical_term: string;
  english_term: string;
  hindi_term: string | null;
  bengali_term: string | null;
  plain_language_explanation: string | null;
  technical_definition: string | null;
  related_statutes: string[] | null;
};
