"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { supabase } from "@/lib/supabase";

type Conversation = {
  id: string;
  title: string | null;
  persona: string;
  language: string;
  jurisdiction_state: string | null;
  created_at: string;
  updated_at: string;
};

type CaseItem = {
  id: string;
  title: string;
  court_name: string | null;
  case_number: string | null;
  matter_type: string | null;
  jurisdiction_state: string | null;
  status: string;
  created_at: string;
};

export default function DashboardPage() {
  const { user, profile, loading } = useAuth();
  const router = useRouter();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  useEffect(() => {
    if (!user || !supabase || !profile) return;

    async function loadData() {
      const [convRes, casesRes] = await Promise.all([
        supabase!.from("conversations")
          .select("*")
          .eq("user_id", profile!.id)
          .order("updated_at", { ascending: false })
          .limit(20),
        supabase!.from("legal_cases")
          .select("*")
          .eq("created_by", profile!.id)
          .order("created_at", { ascending: false })
          .limit(20),
      ]);

      if (convRes.data) setConversations(convRes.data as Conversation[]);
      if (casesRes.data) setCases(casesRes.data as CaseItem[]);
      setLoadingData(false);
    }

    loadData();
  }, [user, profile]);

  if (loading || !user) {
    return <section className="tile-light"><p className="text-caption text-ink-muted-48">Loading…</p></section>;
  }

  return (
    <>
      <section className="tile-parchment">
        <div className="mx-auto max-w-content">
          <h1 className="headline-tight text-display-lg text-ink">
            Welcome, {profile?.full_name || user.email?.split("@")[0]}.
          </h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            {profile?.role === "advocate" ? "Advocate workspace" : "Your legal assistant dashboard"}
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link href="/ask" className="btn-primary">New conversation</Link>
            {profile?.role === "advocate" && (
              <Link href="/advocate" className="btn-secondary">Advocate tools</Link>
            )}
            <Link href="/dashboard/profile" className="btn-pearl">Edit profile</Link>
          </div>
        </div>
      </section>

      <section className="bg-canvas px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content space-y-10">
          {/* Recent Conversations */}
          <div>
            <p className="text-body-strong text-ink">Recent conversations</p>
            <p className="mt-1 text-caption text-ink-muted-48">
              {conversations.length} conversation{conversations.length !== 1 ? "s" : ""}
            </p>
            {loadingData ? (
              <p className="mt-4 text-caption text-ink-muted-48">Loading…</p>
            ) : conversations.length === 0 ? (
              <div className="mt-4 utility-card text-center">
                <p className="text-caption text-ink-muted-48">No conversations yet.</p>
                <Link href="/ask" className="btn-primary mt-4 inline-block">Start your first conversation</Link>
              </div>
            ) : (
              <div className="mt-4 space-y-2">
                {conversations.map((conv) => (
                  <Link
                    key={conv.id}
                    href={`/ask?conversation=${conv.id}`}
                    className="utility-card block text-left transition-colors hover:border-primary"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-caption-strong text-ink">
                          {conv.title || "Untitled conversation"}
                        </p>
                        <p className="mt-1 text-micro-legal text-ink-muted-48">
                          {conv.persona} · {conv.language} · {new Date(conv.updated_at).toLocaleDateString()}
                        </p>
                      </div>
                      {conv.jurisdiction_state && (
                        <span className="text-micro-legal text-ink-muted-48">{conv.jurisdiction_state}</span>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Cases — advocate only */}
          {profile?.role === "advocate" && (
            <div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-body-strong text-ink">Your cases</p>
                  <p className="mt-1 text-caption text-ink-muted-48">
                    {cases.length} case{cases.length !== 1 ? "s" : ""}
                  </p>
                </div>
                <Link href="/advocate/cases" className="btn-pearl">View all</Link>
              </div>
              {cases.length === 0 ? (
                <div className="mt-4 utility-card text-center">
                  <p className="text-caption text-ink-muted-48">No cases yet.</p>
                  <Link href="/advocate" className="btn-primary mt-4 inline-block">Create a case</Link>
                </div>
              ) : (
                <div className="mt-4 space-y-2">
                  {cases.map((c) => (
                    <Link
                      key={c.id}
                      href={`/advocate/cases/${c.id}`}
                      className="utility-card block text-left transition-colors hover:border-primary"
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="text-caption-strong text-ink">{c.title}</p>
                          <p className="mt-1 text-micro-legal text-ink-muted-48">
                            {[c.court_name, c.case_number, c.matter_type].filter(Boolean).join(" · ")}
                          </p>
                        </div>
                        <span className={`text-micro-legal ${c.status === "active" ? "text-success" : "text-ink-muted-48"}`}>
                          {c.status}
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </section>
    </>
  );
}
