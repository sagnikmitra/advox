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
    <div className="dark-card">
      <h3 className="text-lg font-medium">Risk Radar</h3>
      <ul className="mt-3 grid gap-2 text-sm text-[#d8d4ce] md:grid-cols-2">
        {RISKS.map((risk) => (
          <li key={risk} className="rounded border border-[#3c3935] px-3 py-2">
            {risk}
          </li>
        ))}
      </ul>
    </div>
  );
}
