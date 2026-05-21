"use client";

import { useEffect, useState, useRef } from "react";
import { useSearchParams } from "next/navigation";
import { runScenario, routeMessage } from "@/lib/api";
import { TRANSITION_WARNING } from "@/lib/constants";
import { useAuth } from "@/lib/auth";
import { supabase } from "@/lib/supabase";
import { MarkdownContent } from "@/components/markdown-content";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  route?: string;
  blocked?: boolean;
  created_at: string;
};

export function LegalChat({ persona }: { persona: "layman" | "advocate" }) {
  const { user, profile } = useAuth();
  const searchParams = useSearchParams();
  const [message, setMessage] = useState("");
  const [state, setState] = useState("");
  const [incidentDate, setIncidentDate] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (profile?.default_state) setState(profile.default_state);
  }, [profile]);

  useEffect(() => {
    const convId = searchParams.get("conversation");
    if (convId && supabase) {
      setConversationId(convId);
      supabase
        .from("conversation_messages")
        .select("id, role, content, route, blocked, created_at")
        .eq("conversation_id", convId)
        .order("created_at")
        .then(({ data }) => {
          if (data) setMessages(data as Message[]);
        });
    }
  }, [searchParams]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function ensureConversation(): Promise<string | null> {
    if (conversationId) return conversationId;
    if (!supabase || !profile) return null;

    const { data, error: err } = await supabase
      .from("conversations")
      .insert({
        user_id: profile.id,
        title: message.slice(0, 80),
        persona,
        language: "en",
        jurisdiction_state: state || null,
      })
      .select("id")
      .single();

    if (err || !data) return null;
    setConversationId(data.id);
    return data.id;
  }

  async function saveMessage(convId: string, msg: Omit<Message, "id" | "created_at">) {
    if (!supabase) return;
    await supabase.from("conversation_messages").insert({
      conversation_id: convId,
      role: msg.role,
      content: msg.content,
      route: msg.route || null,
      blocked: msg.blocked || false,
    });
    await supabase
      .from("conversations")
      .update({ updated_at: new Date().toISOString() })
      .eq("id", convId);
  }

  async function handleRun() {
    if (!message.trim() || message.trim().length < 5) return;
    setLoading(true);
    setError("");

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: message,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    const currentMessage = message;
    setMessage("");

    try {
      const payload = {
        message: currentMessage,
        persona,
        language: "en",
        state: state || null,
        incident_date: incidentDate || null,
        documents: [],
      };

      const routing = await routeMessage(payload);
      const scenario = await runScenario(payload);

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: scenario.content,
        route: routing.route,
        blocked: scenario.blocked,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);

      if (user && profile) {
        const convId = await ensureConversation();
        if (convId) {
          await saveMessage(convId, { role: "user", content: currentMessage });
          await saveMessage(convId, {
            role: "assistant",
            content: scenario.content,
            route: routing.route,
            blocked: scenario.blocked,
          });
        }
      }
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

      {/* Message history */}
      {messages.length > 0 && (
        <div className="mt-4 max-h-[500px] space-y-3 overflow-y-auto rounded-lg border border-hairline bg-canvas p-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`rounded-lg p-3 ${
                msg.role === "user"
                  ? "ml-8 bg-primary/5 text-right"
                  : "mr-8 bg-canvas-parchment"
              }`}
            >
              <p className="text-micro-legal text-ink-muted-48 mb-1">
                {msg.role === "user" ? "You" : "Advox"}
                {msg.route && ` · ${msg.route}`}
              </p>
              {msg.role === "assistant" ? (
                <MarkdownContent content={msg.content} />
              ) : (
                <p className="text-caption text-ink-muted-80">{msg.content}</p>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}

      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleRun();
          }
        }}
        className="mt-3 w-full rounded-lg border border-hairline bg-canvas px-4 py-3 text-body text-ink outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
        rows={3}
        placeholder={
          messages.length > 0
            ? "Follow-up question…"
            : "Describe legal situation, jurisdiction, dates, and documents"
        }
      />
      <p className="mt-2 text-caption text-warning">{TRANSITION_WARNING}</p>

      <div className="mt-4 flex items-center gap-3">
        <button
          onClick={handleRun}
          disabled={loading || message.trim().length < 5}
          className="btn-primary disabled:opacity-50"
        >
          {loading ? "Running…" : messages.length > 0 ? "Send" : "Run legal workflow"}
        </button>
        {!user && (
          <p className="text-micro-legal text-ink-muted-48">
            Sign in to save conversation history
          </p>
        )}
      </div>

      {error && <p className="mt-3 text-caption text-error">{error}</p>}
    </div>
  );
}
