const STATES = ["Delhi", "West Bengal", "Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat"];

export function JurisdictionSelector() {
  return (
    <select className="input-rect" defaultValue="">
      <option value="">Select State</option>
      {STATES.map((state) => (
        <option key={state} value={state}>{state}</option>
      ))}
    </select>
  );
}
