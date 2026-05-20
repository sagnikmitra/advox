"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { supabase } from "@/lib/supabase";

export default function ProfilePage() {
  const { user, profile, loading } = useAuth();
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [preferredLanguage, setPreferredLanguage] = useState("en");
  const [defaultState, setDefaultState] = useState("");
  const [barCouncilId, setBarCouncilId] = useState("");
  const [enrollmentNumber, setEnrollmentNumber] = useState("");
  const [practiceAreas, setPracticeAreas] = useState("");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!loading && !user) router.push("/login");
  }, [loading, user, router]);

  useEffect(() => {
    if (!profile) return;
    setFullName(profile.full_name || "");
    setPreferredLanguage(profile.preferred_language || "en");
    setDefaultState(profile.default_state || "");

    if (profile.role === "advocate" && supabase) {
      supabase
        .from("advocate_profiles")
        .select("bar_council_id, enrollment_number, practice_areas")
        .eq("user_id", profile.id)
        .single()
        .then(({ data }) => {
          if (data) {
            setBarCouncilId(data.bar_council_id || "");
            setEnrollmentNumber(data.enrollment_number || "");
            setPracticeAreas((data.practice_areas || []).join(", "));
          }
        });
    }
  }, [profile]);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase || !profile) return;
    setSaving(true);
    setError("");
    setSaved(false);

    const { error: userErr } = await supabase
      .from("users")
      .update({
        full_name: fullName,
        preferred_language: preferredLanguage,
        default_state: defaultState || null,
      })
      .eq("id", profile.id);

    if (userErr) {
      setError(userErr.message);
      setSaving(false);
      return;
    }

    if (profile.role === "advocate") {
      const advocateData = {
        user_id: profile.id,
        bar_council_id: barCouncilId || null,
        enrollment_number: enrollmentNumber || null,
        practice_areas: practiceAreas ? practiceAreas.split(",").map((s) => s.trim()) : [],
      };

      const { data: existing } = await supabase
        .from("advocate_profiles")
        .select("id")
        .eq("user_id", profile.id)
        .single();

      if (existing) {
        await supabase.from("advocate_profiles").update(advocateData).eq("user_id", profile.id);
      } else {
        await supabase.from("advocate_profiles").insert(advocateData);
      }
    }

    setSaving(false);
    setSaved(true);
  }

  if (loading || !user) {
    return <section className="tile-light"><p className="text-caption text-ink-muted-48">Loading…</p></section>;
  }

  return (
    <section className="tile-light">
      <div className="mx-auto max-w-[500px] text-left">
        <Link href="/dashboard" className="text-caption text-primary hover:underline">&larr; Dashboard</Link>
        <h1 className="headline-tight mt-4 text-display-lg text-ink">Profile.</h1>

        <form onSubmit={handleSave} className="mt-8 space-y-4">
          <div>
            <label className="text-caption-strong text-ink">Full name</label>
            <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)}
              className="input-rect mt-1 w-full" />
          </div>
          <div>
            <label className="text-caption-strong text-ink">Email</label>
            <input type="email" value={user.email || ""} disabled
              className="input-rect mt-1 w-full opacity-60" />
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-caption-strong text-ink">Preferred language</label>
              <select value={preferredLanguage} onChange={(e) => setPreferredLanguage(e.target.value)}
                className="input-rect mt-1 w-full">
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="bn">Bengali</option>
              </select>
            </div>
            <div>
              <label className="text-caption-strong text-ink">Default state</label>
              <input type="text" value={defaultState} onChange={(e) => setDefaultState(e.target.value)}
                className="input-rect mt-1 w-full" placeholder="e.g. Maharashtra" />
            </div>
          </div>

          <div className="rounded-lg border border-hairline bg-canvas-parchment p-4">
            <p className="text-caption-strong text-ink">Role: {profile?.role}</p>
            <p className="text-micro-legal text-ink-muted-48 mt-1">
              {profile?.role === "advocate" ? "Advocate account with access to research and case tools." : "Citizen account with access to legal guidance."}
            </p>
          </div>

          {profile?.role === "advocate" && (
            <>
              <div className="border-t border-hairline pt-4">
                <p className="text-body-strong text-ink">Advocate details</p>
              </div>
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="text-caption-strong text-ink">Bar Council ID</label>
                  <input type="text" value={barCouncilId} onChange={(e) => setBarCouncilId(e.target.value)}
                    className="input-rect mt-1 w-full" placeholder="e.g. MAH/1234/2020" />
                </div>
                <div>
                  <label className="text-caption-strong text-ink">Enrollment number</label>
                  <input type="text" value={enrollmentNumber} onChange={(e) => setEnrollmentNumber(e.target.value)}
                    className="input-rect mt-1 w-full" />
                </div>
              </div>
              <div>
                <label className="text-caption-strong text-ink">Practice areas</label>
                <input type="text" value={practiceAreas} onChange={(e) => setPracticeAreas(e.target.value)}
                  className="input-rect mt-1 w-full" placeholder="Criminal, Family, Property (comma-separated)" />
              </div>
            </>
          )}

          {error && <p className="text-caption text-error">{error}</p>}
          {saved && <p className="text-caption text-success">Profile saved.</p>}

          <button type="submit" disabled={saving} className="btn-primary w-full disabled:opacity-50">
            {saving ? "Saving…" : "Save profile"}
          </button>
        </form>
      </div>
    </section>
  );
}
