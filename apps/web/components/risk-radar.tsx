const RISKS = [
  "Missed deadlines",
  "Jurisdiction defects",
  "Limitation risk",
  "Weak evidence",
  "Procedural non-compliance",
  "BNS/IPC transition mismatch"
];

export function RiskRadar() {
  return (
    <div className="rounded-lg bg-surface-tile-1 p-6">
      <p className="text-body-strong text-on-dark">Risk Radar</p>
      <ul className="mt-4 grid gap-2 md:grid-cols-2">
        {RISKS.map((risk) => (
          <li key={risk} className="rounded-sm border border-[rgba(255,255,255,0.08)] px-4 py-3 text-caption text-body-muted">
            {risk}
          </li>
        ))}
      </ul>
    </div>
  );
}
