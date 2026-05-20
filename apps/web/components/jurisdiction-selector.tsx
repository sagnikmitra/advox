const STATES = ["Delhi", "West Bengal", "Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat"];

export function JurisdictionSelector() {
  return (
    <select className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm text-ink" defaultValue="">
      <option value="">Select State</option>
      {STATES.map((state) => (
        <option key={state} value={state}>
          {state}
        </option>
      ))}
    </select>
  );
}
