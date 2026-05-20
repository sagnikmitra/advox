"use client";

import { Suspense } from "react";
import { LegalChat } from "./legal-chat";

export function LegalChatWrapper({ persona }: { persona: "layman" | "advocate" }) {
  return (
    <Suspense fallback={<div className="utility-card"><p className="text-caption text-ink-muted-48">Loading chat…</p></div>}>
      <LegalChat persona={persona} />
    </Suspense>
  );
}
