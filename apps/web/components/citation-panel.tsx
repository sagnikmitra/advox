import type { CitationStatus } from "@/lib/types";

const SAMPLE: { text: string; status: CitationStatus }[] = [
  { text: "[Statute] Bharatiya Nagarik Suraksha Sanhita, 2023 - Section 173 -> verified-source-link", status: "verified" }
];

export function CitationPanel() {
  return (
    <aside className="card">
      <h3 className="text-lg font-medium text-ink">Citation Panel</h3>
      <ul className="mt-3 space-y-2 text-sm text-body">
        {SAMPLE.map((item) => (
          <li key={item.text} className="rounded-md border border-hairline bg-canvas p-3">
            <p>{item.text}</p>
            <p className="mt-1 text-xs uppercase tracking-wide text-muted">status: {item.status}</p>
          </li>
        ))}
      </ul>
    </aside>
  );
}
