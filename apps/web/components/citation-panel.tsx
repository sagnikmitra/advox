import type { CitationStatus } from "@/lib/types";

const SAMPLE: { text: string; status: CitationStatus }[] = [
  { text: "[Statute] Bharatiya Nagarik Suraksha Sanhita, 2023 - Section 173 -> verified-source-link", status: "verified" }
];

const STATUS_STYLES: Record<CitationStatus, string> = {
  verified: "text-success",
  partially_verified: "text-warning",
  unverified: "text-ink-muted-48",
  conflicting: "text-error",
  missing: "text-error",
};

export function CitationPanel() {
  return (
    <aside className="utility-card">
      <p className="text-body-strong text-ink">Citation Panel</p>
      <ul className="mt-4 space-y-3">
        {SAMPLE.map((item) => (
          <li key={item.text} className="rounded-lg border border-hairline bg-canvas-parchment p-4">
            <p className="text-caption text-ink-muted-80">{item.text}</p>
            <p className={`mt-1 text-caption-strong ${STATUS_STYLES[item.status]}`}>
              {item.status}
            </p>
          </li>
        ))}
      </ul>
    </aside>
  );
}
